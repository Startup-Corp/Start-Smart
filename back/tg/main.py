from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import configparser
import asyncio

# Загрузка конфигурации
config = configparser.ConfigParser()
config.read('../../config.ini')
api_key = config['tg_key']['api_key']

# Инициализация FastAPI и aiogram
app = FastAPI()
bot = Bot(token=api_key)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(Command('start'))
async def handle_start(message: Message):
    await message.answer("Привет! Я бот для верификации ответов нейросети.")

# Эндпоинт для отправки сообщений
@app.post("/send_message")
async def send_message(request: Request):
    data = await request.json()
    user_id = data.get('user_id')
    response = data.get('response')
    await bot.send_message(user_id, f"Ответ от нейросети: {response}")
    return {"status": "success"}

# Запуск бота
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    # Запуск FastAPI и aiogram
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    
    await asyncio.gather(
        server.serve(),
        on_startup()
    )

if __name__ == "__main__":
    import uvicorn
    asyncio.run(main())
