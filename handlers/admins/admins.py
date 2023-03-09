from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import database.models
import states.AllStates
from loader import bot
from data.config import ADMINS
from states.AllStates import *
from database.connections import *


async def start_admin_handler(message: Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        await message.answer("Xabaringizni yozing adminjon")
        await states.AllStates.UserStates.admin.set()


async def admin_text_state(message: Message, state: FSMContext):
    text = message.text
    if text == "users":
        await message.answer(database.models.Users.user_id)

# state uchun handler yaratiladi
# admin yuborgan text olasila
# bazadan barcha userlar id sini olasila
# for orqali userlarni idsini bita bita olvolasilar
# user idsi orqali userga admin textini yuborasilar


def register_admins_py(dp: Dispatcher):
    dp.register_message_handler(start_admin_handler, commands=['admin'])
    dp.register_message_handler(admin_text_state, text='users')
