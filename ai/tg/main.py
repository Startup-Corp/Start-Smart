import sys
import os
import configparser
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from objects.dbManager import DB_manager

# Загрузка конфигурации
config = configparser.ConfigParser()
config.read('../../config.ini')
api_key = config['tg_key']['api_key']


# Инициализация FastAPI и aiogram
app = FastAPI()
bot = Bot(token=api_key)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
# db = DB_manager(config['supabase']['url'], config['supabase']['key'])

# Обработчик команды /start
@dp.message(Command('start'))
async def handle_start(message: types.Message):
    id = message.chat.id
    await message.answer(f"Привет! Я бот для верификации ответов нейросети. {id}")

# Обработчик нажатий на инлайн-кнопки
@dp.callback_query(lambda c: c.data and c.data.startswith('approve_'))
async def process_callback_approve(callback_query: types.CallbackQuery):
    action, request_id = callback_query.data.split('_')[1], callback_query.data.split('_')[2]
    if action == 'yes':
        await bot.send_message(callback_query.from_user.id, "Вы одобрили ответ.")
        db.update("Requests", {"verified": True}, {"id": request_id})
    elif action == 'no':
        await bot.send_message(callback_query.from_user.id, "Вы отклонили ответ.")
    await callback_query.answer()

@app.post("/approve")
async def approve(request: Request):
    data = await request.json()
    user_id = '713091230'
    response = data.get('response')
    request_id = data.get('request_id')
    print(f'approve: {response}')

    # Создание инлайн-кнопок
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Approve', callback_data='approve_yes{request_id}'),
        InlineKeyboardButton(text='Disapprove', callback_data='approve_no{request_id}')
    )

    # Отправка сообщения с инлайн-кнопками
    await bot.send_message(user_id, f"Ответ от нейросети: {response}", reply_markup=builder.as_markup())
    
    return {"status": "success"}

# Запуск бота
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    # Запуск FastAPI и aiogram
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    
    await asyncio.gather(
        server.serve(),
        on_startup()
    )

if __name__ == "__main__":
    import uvicorn
    asyncio.run(main())
