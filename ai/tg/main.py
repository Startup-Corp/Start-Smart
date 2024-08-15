import asyncio
import configparser
import sys
import os
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import InlineKeyboardButton, FSInputFile, ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

absolute_path_to_objects = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../back/objects'))
sys.path.append(absolute_path_to_objects)

from dbManager import db

config = configparser.ConfigParser()
config.read('../config.ini')
api_key = config['tg_key']['api_key']

bot = Bot(token=api_key)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

class FileState(StatesGroup):
    waiting_file = State()

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

@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Привет. Я предоставляю функционал одобрения ответов проекта Start-Smart')

@router.message(Command('id'))
async def get_id(message: types.Message):
    await message.answer(f'Your id = {message.from_user.id}, chat_id = {message.chat.id}, thread={message.message_thread_id}')

@router.callback_query(lambda c: c.data and c.data.startswith('approve_'))
async def process_callback_approve(callback_query: types.CallbackQuery, state: FSMContext):
    action, project_id = callback_query.data.split('_')[1], callback_query.data.split('_')[2]
    project_id = int(project_id)
    
    if action == 'yes':
        await bot.send_message('-1002244887628', "Вы одобрили файл.", message_thread_id=2)
        db.update("Projects", {"verified": True}, {"id": project_id})
    elif action == 'no':
        await bot.send_message('-1002244887628', "Вы отклонили файл. Пожалуйста, отправьте исправленный файл.", message_thread_id=2)
        await state.set_state(FileState.waiting_file)
    
    await callback_query.answer()

@router.message(FileState.waiting_file, F.document)
async def get_document(message: types.Message, state: FSMContext):
    name = 'report'
    path = rf"D:\code\Start-Smart\ai\fixed_{name}.md"
    
    document = message.document
    file = await bot.get_file(document.file_id)
    await bot.download_file(file.file_path, destination=path)
    
    await bot.send_message('-1002244887628', "Файл скачан", message_thread_id=2)
    await state.clear()

async def run_dp():
    await dp.start_polling(bot)
