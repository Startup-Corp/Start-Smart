# back/tg/handlers.py
from aiogram import types, Router
from aiogram.filters import Command
from main import bot

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот для верификации ответов нейросети.")

@router.post("/send_message")
async def send_message(request: types.Request):
    data = await request.json()
    user_id = data.get('user_id')
    response = data.get('response')
    await bot.send_message(user_id, f"Ответ от нейросети: {response}")
