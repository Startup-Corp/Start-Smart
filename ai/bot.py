import asyncio
import configparser
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

from objects.project import UploadReport, UpdateVerified, UpdateProjectStatus

base_url = 'http://127.0.0.1:5001'

config = configparser.ConfigParser()
config.read('config.ini')

IS_DEV = True if config['main']['is_dev'] == 'True' else False

if IS_DEV:
    api_key = config['tg_key']['dev_key']
else:
    api_key = config['tg_key']['prod_key']

chat_id = config['tg_key']['chat_id']
topic_id = config['tg_key']['topic_id']

bot = Bot(token=api_key)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

class ApprovalState(StatesGroup):
    waiting_for_file = State()

async def start_approval(file_data: bytes, project_id: str, user_id: str, bucket_id: str, email: str):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Approve', callback_data=f'approve|{project_id}'),
        InlineKeyboardButton(text='Disapprove', callback_data=f'disapprove|{project_id}'),
        InlineKeyboardButton(text='Disfile', callback_data=f'disfile|{project_id}|{bucket_id}'),
        InlineKeyboardButton(text='Restart', callback_data=f'restart|{project_id}|{user_id}|{email}')
    )
    #print(len(f'restart|{project_id}|{user_id}|{email}'.encode('utf-8')))
    file = BufferedInputFile(file_data, f'user_{user_id[:5]}_pr_{project_id}.md')
    UpdateProjectStatus.execute(project_id, 'Human')

    logging.info(f'Bot. Send file of pr_id: {project_id} in dev chat.')
    await bot.send_document(chat_id, file, message_thread_id=topic_id)
    await bot.send_message(
        chat_id=chat_id,
        text="Файл на проверку",
        reply_markup=builder.as_markup(),
        message_thread_id=topic_id
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

    if action == 'approve':
        logging.info(f'Bot. Approve file of pr_id: {project_id} in dev chat.')
        await bot.send_message(chat_id, "Вы одобрили файл.", message_thread_id=topic_id)
        UpdateProjectStatus.execute(project_id, 'Done')
        UpdateVerified.execute(project_id, verified=True)
        await state.clear()
    elif action == 'disapprove':
        logging.info(f'Bot. Disapprove file of pr_id: {project_id} in dev chat.')
        await bot.send_message(chat_id, "Вы отклонили файл.", message_thread_id=topic_id)
        await state.clear()
    elif action == 'disfile':
        bucket_id = callback_query.data.split('|')[2]
        logging.info(f'Bot. Disfile file of pr_id: {project_id} in dev chat.')
        await bot.send_message(chat_id, "Вы отклонили файл. Пожалуйста, отправьте исправленный файл.", message_thread_id=topic_id)
        await state.set_state(ApprovalState.waiting_for_file)
        await state.update_data(bucket_id=bucket_id, project_id=project_id)
    elif action == 'restart':
        user_id = callback_query.data.split('|')[2]
        email = callback_query.data.split('|')[3]
        logging.info(f'Bot. Restart file of pr_id: {project_id} in dev chat.')
        await bot.send_message(chat_id, "Restart", message_thread_id=topic_id)
        
        response = requests.post(
            f'{base_url}/create_report',
            json = {
            'project_id': project_id,
            'user_id': user_id,
            'email': email
        })
        if response.status_code == 200:
            await bot.send_message(chat_id, "gpt flow перезапущен", message_thread_id=topic_id)
        else:
            await bot.send_message(chat_id, "gpt flow не удалось перезапустить", message_thread_id=topic_id)
    await callback_query.answer()


@router.message(ApprovalState.waiting_for_file, F.document)
async def get_document(message: types.Message, state: FSMContext):
    data = await state.get_data()
    project_id = data.get('project_id')
    bucket_id = data.get('bucket_id')

    logging.info(f'Bot. New file of pr_id: {project_id} in dev chat.')

    if project_id is None or bucket_id is None:
        await bot.send_message(chat_id, "Missing project_id or bucket_id", message_thread_id=topic_id)
        return

    document = message.document
    file = await bot.get_file(document.file_id)
    result: io.BytesIO = await bot.download_file(file.file_path)
    filename = 'result.md' if '.md' in file.file_path else 'result.pdf'

    UploadReport.execute(bucket_id, project_id, result.read(), filename)
    
    await bot.send_message(chat_id, "File uploaded successfully.", message_thread_id=topic_id)
    UpdateProjectStatus.execute(project_id, 'Done')
    await state.clear()

if __name__ == '__main__':
    logging.basicConfig(filename="bot.log",
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    filemode="w")
    asyncio.run(dp.start_polling(bot))