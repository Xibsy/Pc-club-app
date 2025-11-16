import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (Message, ReplyKeyboardMarkup, InlineKeyboardButton,
                           InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery, CallbackQuery)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from constants import ADMIN_CHAT_ID, TOKEN, START_BUTTONS, COMPUTERS_RESERVATION_BUTTONS, DATE_RANGE
from sql import IsNewUser, Database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)


class Reservation(StatesGroup):
    computer = State()
    date = State()
    time = State()


class Feedback(StatesGroup):
    message = State()


class BotHandler:
    def __init__(self):
        self._bot = Bot(
            token=TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self._dp = Dispatcher()
        self._register_handlers()

        self._database = Database()

    def _register_handlers(self):
        self._dp.message.register(self.feedback, F.text == '💻 Написать разработчику')
        self._dp.message.register(self.send_feedback_to_admin, Feedback.message)

        self._dp.message.register(self.admin_helps_command, F.text == '⚙ Админ панель')
        self._dp.message.register(self.broadcast, Command('br'), F.from_user.id == ADMIN_CHAT_ID)
        self._dp.message.register(self.ls_message, Command('answer'), F.from_user.id == ADMIN_CHAT_ID)

        self._dp.message.register(self.command_start_handler, F.text.in_({'/start', 'Назад'}))
        self._dp.message.register(self.reservation_block, F.text == '🖥 Забронировать компьютер')
        self._dp.callback_query.register(self.set_reservation_date, F.data.in_({str(_) for _ in range(1, 7)}))
        self._dp.callback_query.register(self.set_reservation_time, F.data.in_(DATE_RANGE))
        self._dp.message.register(self.end_reservation)

    @staticmethod
    def create_pc_reservation_buttons() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for button in COMPUTERS_RESERVATION_BUTTONS:
            builder.button(text=button, callback_data=f'{COMPUTERS_RESERVATION_BUTTONS.index(button) + 1}')
        builder.adjust(3, 3, 1)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def create_dates_buttons() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for date in DATE_RANGE:
            builder.button(text=date, callback_data=date)
        builder.button(text='Назад', callback_data='back')
        builder.adjust(3, 3, 1, 1)
        return builder.as_markup(resize_keyboard=True)

    async def command_start_handler(self, message: Message) -> None:
        if IsNewUser(message.chat.id).check:
            self._database.append_new_user(message.from_user.username, message.from_user.id, 1)
        user_name = html.bold(message.from_user.full_name)

        keyboard = ReplyKeyboardMarkup(keyboard=START_BUTTONS, resize_keyboard=True,
                                       input_field_placeholder="Воспользуйтесь меню:")

        if message.chat.id != ADMIN_CHAT_ID:
            keyboard = ReplyKeyboardMarkup(keyboard=START_BUTTONS[:2], resize_keyboard=True,
                                           input_field_placeholder="Воспользуйтесь меню:")

        await message.answer(
            f"🖐 Привет, {user_name}!\n\n"
            f"Ты попал в телеграм бота нашего пк клуба!\n\n"
            f"Выбери действия ниже 👇",
            reply_markup=keyboard
        )

    async def reservation_block(self,
                                message: Message,
                                state: FSMContext) -> None:
        await state.set_state(Reservation.computer)
        await message.answer(f'Выберите компьютер 💻', reply_markup=self.create_pc_reservation_buttons())

    async def set_reservation_date(self, callback: CallbackQuery,
                                state: FSMContext) -> None:
        await callback.answer()
        await state.update_data(computer=callback.data)
        await callback.message.edit_text(text='Выберите дату 📅', reply_markup=self.create_dates_buttons())

    async def set_reservation_time(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await state.update_data(date=callback.data)
        await callback.message.edit_text(text=f'Напишите удобное вам время в форма Часы:Минуты\n'
                                              f'{html.quote('Пример: 09:41')}')

    async def end_reservation(self, message: Message, state: FSMContext) -> None:
        await state.update_data(time=message.text)
        data = await state.get_data()
        await message.answer(f'Ваша бронь на {data['time']}, {data['date']} числа, место {data['computer']}')
        self._database.append_reservation(int(data['computer']), message.from_user.username, data['date'], data['time'])
        await state.clear()

    async def feedback(self, message: Message, state: FSMContext) -> None:
        await state.set_state(Feedback.message)
        await message.answer(f'Напишите свой отзыв/баг/и т.д.\n\n{html.bold('Только текстовые сообщения')}')

    async def send_feedback_to_admin(self, message: Message, state: FSMContext) -> None:
        await state.update_data(message=message.text)
        data = await state.get_data()
        await message.answer('Сообщение успешно отправлено')
        await self._bot.send_message(ADMIN_CHAT_ID, f'{message.from_user.username}: {data['message']}')
        await state.clear()

    async def broadcast(self, message: Message, command: CommandObject) -> None:
        broadcast_text = command.args
        users_chats = self._database.chats_ids
        for id in users_chats:
            if id == ADMIN_CHAT_ID:
                continue
            await self._bot.send_message(id, broadcast_text)
        await message.answer(f'Вы отправили всем сообщение {html.bold(broadcast_text)}')

    async def ls_message(self, message: Message, command: CommandObject):
        broadcast_text = command.args.split(', ')
        await self._bot.send_message(self._database.get_chat_id(broadcast_text[0]),
                                    f'⚙ Администратор отправил вам сообщение: {html.bold(broadcast_text[1])}')

    async def admin_helps_command(self, message: Message) -> None:
        help_text = f"""
/br (сообщение) - отправить всем пользователям сообщение
/answer (юзернейм), (сообщение) - отправить сообщение конкретному пользователю
    """
        await message.answer(help_text)

    async def main(self) -> None:
        logger = logging.getLogger(__name__)
        logger.info("Запуск бота....")

        try:
            self._database.start_bd()
            await self._dp.start_polling(self._bot)
        except Exception as exception:
            logger.error(f"Ошибка: {exception}")
        finally:
            await self._bot.session.close()
            logger.info("Бот остановлен")


if __name__ == "__main__":
    bot_handler = BotHandler()
    try:
        asyncio.run(bot_handler.main())
    except KeyboardInterrupt:
        print("\nОстановлен пользователем")
    except Exception as exception:
        logging.error(f"Непредвидинная ошибка: {exception}")