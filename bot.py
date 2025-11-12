import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup
from constants import ADMIN_CHAT_ID, TOKEN, START_BUTTONS
from sql import IsNewUser, Database


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

database = Database()

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if IsNewUser(message.chat.id).check:
        database.append_new_user(message.from_user.username, message.from_user.id, 1)
    user_name = html.bold(message.from_user.full_name)
    keyboard = ReplyKeyboardMarkup(keyboard=START_BUTTONS, resize_keyboard=True)
    if message.chat.id != ADMIN_CHAT_ID:
        keyboard = ReplyKeyboardMarkup(keyboard=START_BUTTONS[:3], resize_keyboard=True)
    await message.answer(
        f"🖐 Привет, {user_name}!\n\n"
        f"Выбери действия ниже 👇",
        reply_markup=keyboard
    )


@dp.message(Command('br'), F.from_user.id == ADMIN_CHAT_ID)
async def broadcast(message: Message, command: CommandObject) -> None:
    broadcast_text = command.args
    users_chats = database.chats_ids
    for id in users_chats:
        if id == ADMIN_CHAT_ID:
            continue
        await bot.send_message(id, broadcast_text)
    await message.answer(f'Вы отправили всем сообщение {html.bold(broadcast_text)}')


@dp.message(Command('tests'), F.from_user.id == ADMIN_CHAT_ID)
async def get_chat_id(message: Message, command: CommandObject):
    broadcast_text = command.args
    await message.answer(f'{database.get_chat_id(broadcast_text)}')


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    help_text = f"""
/kaki
    """
    await message.answer(help_text)


@dp.message(F.from_user.id != ADMIN_CHAT_ID)
async def echo(message: Message) -> None:
     await bot.send_message(ADMIN_CHAT_ID, f'{message.from_user.full_name}: {message.text}')


async def main() -> None:
    logger = logging.getLogger(__name__)
    logger.info("Запуск бота....")

    try:
        database.start_bd()
        await dp.start_polling(bot)
    except Exception as exception:
        logger.error(f"Ошибка: {exception}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nОстановлен пользователем")
    except Exception as exception:
        logging.error(f"Непредвидинная ошибка: {exception}")
