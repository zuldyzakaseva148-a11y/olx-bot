import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "9281348613:AAGIf_CvqbFmablkeXgkAcyHn5UFu-ClRG4"
CHAT_ID = 7525212274

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Бот-радар OLX Караганда успешно запущен и работает!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен и слушает сервер...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
