import asyncio
import configparser
import os
import requests
import logging
import io
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from back.objects.dbManager import DB_manager
from objects.project import UploadReport, UpdateVerified, UpdateProjectStatus

base_url = 'http://127.0.0.1:5002'

db = DB_manager()
config = configparser.ConfigParser()
config.read('config.ini')

IS_DEV = True if config['main']['is_dev'] == 'True' else False

if IS_DEV:
    api_key = config['tg_key']['devv_key']
else:
    api_key = config['tg_key']['prod_key']


chat_id = config['tg_key']['chat_id']
logging.info(f'chat_id {chat_id}')

bot = Bot(token=api_key)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

class ApprovalState(StatesGroup):
    waiting_for_file = State()

async def start_approval(file_data: bytes, project_id: str, user_id: str, bucket_id: str):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Approve', callback_data=f'a|{project_id}|{user_id}'),
        InlineKeyboardButton(text='Disapprove', callback_data=f'd|{project_id}|{user_id}'),
        InlineKeyboardButton(text='Disfile', callback_data=f'f|{project_id}|{bucket_id}|{user_id}'),
        InlineKeyboardButton(text='Restart', callback_data=f'r|{project_id}|{user_id}')
    )

    file = BufferedInputFile(file_data, f'user_{user_id[:5]}_pr_{project_id}.md')
    UpdateProjectStatus.execute(project_id, 'Human')

    logging.info(f'Bot. Send file of pr_id: {project_id} in dev chat.')
    await bot.send_document(chat_id, file)

    await bot.send_message(
        chat_id=chat_id,
        text="Файл на проверку",
        reply_markup=builder.as_markup()
    )


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Привет. Я предоставляю функционал одобрения ответов проекта Start-Smart')

@router.message(Command('id'))
async def get_id(message: types.Message):
    await message.answer(f'Your id = {message.from_user.id}, chat_id = {message.chat.id}, thread={message.message_thread_id}')


@router.callback_query()
async def process_callback_approve(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data.split('|')[0]
    project_id = callback_query.data.split('|')[1]

    if action == 'a':
        logging.info(f'Bot. Approve file of pr_id: {project_id} in dev chat.')

        await bot.send_message(chat_id, "Вы одобрили файл.")


        UpdateProjectStatus.execute(project_id, 'Done')
        UpdateVerified.execute(project_id, verified=True)
        await state.clear()
    elif action == 'd':
        logging.info(f'Bot. Disapprove file of pr_id: {project_id} in dev chat.')


        await bot.send_message(chat_id, "Вы отклонили файл.")
        await state.clear()
    elif action == 'f':
        bucket_id = callback_query.data.split('|')[2]
        logging.info(f'Bot. Disfile file of pr_id: {project_id} in dev chat.')
        await bot.send_message(chat_id, "Вы отклонили файл. Пожалуйста, отправьте исправленный файл.")
        await state.set_state(ApprovalState.waiting_for_file)
        await state.update_data(bucket_id=bucket_id, project_id=project_id)
    elif action == 'r':
        email_response = db.select("buckets", schema="storage", columns="name", criteria={"owner": user_id})

        email = email_response.data[0]['name'].split('_')[0] if email_response.data else None
        user_id = callback_query.data.split('|')[2]
        logging.info(f'Bot. Restart file of pr_id: {project_id} in dev chat. User email {email}. User_id {user_id}. Project_id {project_id}')
        await bot.send_message(chat_id, "Restart")


        response = requests.post(
            f'{base_url}/create_report',
            json = {
            'project_id': project_id,
            'user_id': user_id,
            'email': email
        })

        if response.status_code == 200:
            await bot.send_message(chat_id, "gpt flow перезапущен")
        else:
            await bot.send_message(chat_id, "gpt flow не удалось перезапустить")

    await callback_query.answer()


@router.message(ApprovalState.waiting_for_file, F.document)
async def get_document(message: types.Message, state: FSMContext):
    data = await state.get_data()
    project_id = data.get('project_id')
    bucket_id = data.get('bucket_id')

    logging.info(f'Bot. New file of pr_id: {project_id} in dev chat.')

    if project_id is None or bucket_id is None:
        await bot.send_message(chat_id, "Missing project_id or bucket_id")
        return

    document = message.document
    file = await bot.get_file(document.file_id)
    result: io.BytesIO = await bot.download_file(file.file_path)
    filename = 'result.md' if '.md' in file.file_path else 'result.pdf'

    UploadReport.execute(bucket_id, project_id, result.read(), filename)
    
    await bot.send_message(chat_id, "File uploaded successfully.")
    UpdateProjectStatus.execute(project_id, 'Done')
    await state.clear()

if __name__ == '__main__':
    logging.basicConfig(filename="bot.log",
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    filemode="w")
    asyncio.run(dp.start_polling(bot))