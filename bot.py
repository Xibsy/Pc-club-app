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


class BotHandler:
    def __init__(self):
        self._database = Database()
        self._bot = Bot(
            token=TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self._dp = Dispatcher()
        self._router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self._dp.message.register(self.get_inline_btn_link, F.text == 'Давай инлайн!')
        self._dp.message.register(self.command_start_handler, F.text.in_({'/start', 'Назад'}))
        self._dp.message.register(self.user_profile, F.text == '👤 Мой профиль')
        self._dp.message.register(self.reservation_block, F.text == '🖥 Забронировать компьютер')
        self._dp.callback_query.register(self.set_reservation_date, F.data.in_({str(_) for _ in range(1, 7)}))
        self._dp.message.register(self.broadcast, Command('br'), F.from_user.id == ADMIN_CHAT_ID)
        self._dp.message.register(self.get_chat_id, Command('answer'), F.from_user.id == ADMIN_CHAT_ID)
        self._dp.message.register(self.command_help_handler, Command("help"))

        self._dp.message.register(self.send_invoice_handler, F.text == 'Оплатить 100 звёзд ⭐️')
        self._dp.pre_checkout_query.register(self.pre_checkout_handler)
        self._dp.message.register(self.pay_support_handler, Command(commands="paysupport"))

    @staticmethod
    def payment_keyboard():
        builder = InlineKeyboardBuilder()
        builder.button(text=f"Оплатить 100⭐️", pay=True)
        return builder.as_markup()

    @staticmethod
    def payment_keyboard_without_payment():
        builder = ReplyKeyboardBuilder()
        builder.button(text=f"Оплатить 100 звёзд ⭐️")
        builder.button(text=f"Назад")
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def ease_link_kb():
        inline_kb_list = [
            [InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/yakvenalex/')],
            [InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')]]
        return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

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
            keyboard = ReplyKeyboardMarkup(keyboard=START_BUTTONS[:3], resize_keyboard=True,
                                           input_field_placeholder="Воспользуйтесь меню:")

        await message.answer(
            f"🖐 Привет, {user_name}!\n\n"
            f"Ты попал в телеграм бота нашего пк клуба!\n\n"
            f"Выбери действия ниже 👇",
            reply_markup=keyboard
        )

    async def user_profile(self, message: Message) -> None:
        await message.answer(f'Ваш стар баланс {html.bold(self._database.get_stars_balance(message.chat.id))}',
                             reply_markup=self.payment_keyboard_without_payment())

    async def send_invoice_handler(self, message: Message):
        prices = [LabeledPrice(label="XTR", amount=100)]
        await message.answer_invoice(
            title="Пополнить баланс",
            description="Пополнить свой баланс на 100 звёзд!",
            prices=prices,
            provider_token="",
            payload="channel_support",
            currency="XTR",
            reply_markup=self.payment_keyboard(),
        )
        self._database.add_stars(100, message.chat.id)

    async def pre_checkout_handler(self, pre_checkout_query: PreCheckoutQuery):
        await pre_checkout_query.answer(ok=True)
        await self._bot.send_message(ADMIN_CHAT_ID, 'Ещё одна проверочка =)')

    async def pay_support_handler(self, message: Message):
        await message.answer(
            text="Добровольные пожертвования не подразумевают возврат средств, "
                 "однако, если вы очень хотите вернуть средства - свяжитесь с нами.")

    async def get_inline_btn_link(self, message: Message):
        await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=self.ease_link_kb())

    async def reservation_block(self,
                                message: Message,
                                state: FSMContext) -> None:
        await state.set_state(Reservation.computer)
        await message.answer(f'Выберите компьютер 💻', reply_markup=self.create_pc_reservation_buttons())

    async def set_reservation_date(self, callback: CallbackQuery,
                                state: FSMContext) -> None:
        await callback.answer('Вииии')
        await state.update_data(computer=int(callback.data))
        await callback.message.edit_text(text='Выберите дату 📅', reply_markup=self.create_dates_buttons())

    async def set_reservation_time(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.update_data(date=callback.data)
        await callback.message.edit_text(text=f'Напишите удобное вам время в форма Часы:Минуты\n'
                                              f'{html.quote('Пример: 09:41')}')

    async def broadcast(self, message: Message, command: CommandObject) -> None:
        broadcast_text = command.args
        users_chats = self._database.chats_ids
        for id in users_chats:
            if id == ADMIN_CHAT_ID:
                continue
            await self._bot.send_message(id, broadcast_text)
        await message.answer(f'Вы отправили всем сообщение {html.bold(broadcast_text)}')

    async def get_chat_id(self, message: Message, command: CommandObject):
        broadcast_text = command.args.split(', ')
        await self._bot.send_message(self._database.get_chat_id(broadcast_text[0]),
                                    f'⚙ Администратор отправил вам сообщение: {html.bold(broadcast_text[1])}')

    async def command_help_handler(self, message: Message) -> None:
        help_text = f"""
/kaki
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