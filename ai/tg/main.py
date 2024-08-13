import asyncio
import configparser
import sys
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

# Получение абсолютного пути к директории 'back/objects'
absolute_path_to_objects = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../back/objects'))
sys.path.append(absolute_path_to_objects)

from dbManager import db

config = configparser.ConfigParser()
config.read('../config.ini')
api_key = config['tg_key']['api_key']

bot = Bot(token=api_key)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def start_approval(user_id: int, file_path: str, project_id: int, topic_id: int = 2):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Approve', callback_data=f'approve_yes_{project_id}'),
        InlineKeyboardButton(text='Disapprove', callback_data=f'approve_no_{project_id}')
    )
    file = FSInputFile(file_path)
    await bot.send_document(user_id, file, message_thread_id=topic_id)

    await bot.send_message(
        chat_id=user_id, 
        text="Файл на проверку", 
        reply_markup=builder.as_markup(),
        message_thread_id=topic_id)

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Привет. Я предоставляю функционал одобрения ответов проекта Start-Smart')#\nТвой id={}

@dp.message(Command('id'))
async def get_id(message: types.Message):
    await message.answer(f'Your id = {message.from_user.id}, chat_id = {message.chat.id}, thread={message.message_thread_id}')

@dp.callback_query(lambda c: c.data and c.data.startswith('approve_'))
async def process_callback_approve(callback_query: types.CallbackQuery):
    action, project_id = callback_query.data.split('_')[1], callback_query.data.split('_')[2]
    project_id = int(project_id)
    
    if action == 'yes':
        await bot.send_message('-1002244887628', "Вы одобрили файл.", message_thread_id=2)
        db.update("Projects", {"verified": True}, {"id": project_id})
    elif action == 'no':
        await bot.send_message('-1002244887628', "Вы отклонили файл.", message_thread_id=2)
    await callback_query.answer()

async def run_dp():
    await dp.start_polling(bot)
