import datetime
import os

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import *

from data.config import ADMIN_GROUP_ID
from database.connections import add_user, get_all_effects, get_users_info, get_effect
from keyboards.default.users_btn import menu_btn, effects_btn, cancel_support_btn
from loader import dp, bot
from states.AllStates import UserStates
from utils.misc.calculate_dates import calculate_date
from utils.misc.pillow_effect import make_filter_image


async def bot_start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    await add_user(user_id, username, today)
    btn = await menu_btn()
    await message.answer("Assalomu aleykum", reply_markup=btn)


async def back_btn_handler(message: Message):
    btn = await menu_btn()
    await message.answer("Bosh menu", reply_markup=btn)


async def show_effects_handler(message: Message):
    effects = await get_all_effects()
    btn = await effects_btn(effects)
    await message.answer("Effectni tanlang:", reply_markup=btn)


async def show_statistika_handler(message: Message):
    users_date, total_users = await get_users_info()
    days, hours = await calculate_date(users_date)
    context = f"Bot azolar soni: {total_users}\n\n" \
              f"1 soat ichida qushilgan azolar: {hours}\n" \
              f"3 kun ichida qushilgan azolar: {days}"
    await message.answer(context)


async def support_handler(message: Message):
    btn = await cancel_support_btn()
    await message.answer("Xabaringizni yo`llang:", reply_markup=btn)
    await UserStates.support_message.set()


async def support_message_state(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    if text == '❌ Bekor qilish':
        btn = await menu_btn()
        await message.answer("Bosh menu", reply_markup=btn)
    else:
        context = f"<a href='tg://user?id={user_id}'>{user_id}</a>\n\n" \
                  f"<em>{text}</em>"
        await bot.send_message(chat_id=ADMIN_GROUP_ID, text=context)

        await message.answer("Sizning xabaringiz adminlarga yuborildi.")
        await back_btn_handler(message)
    await state.finish()


async def get_selected_effect_handler(message: Message, state: FSMContext):
    text = message.text
    effect = await get_effect(text)
    if effect:
        await state.update_data(effect=effect[0]['effect'])
        await message.answer("Rasim yuboring:")
        await UserStates.get_photo.set()


async def get_user_photo_state(message: Message, state: FSMContext):
    file = await bot.get_file(message.photo[-1].file_id)
    file_type = file.file_path.split(".")[-1]
    filename = f"images/{message.from_user.id}.{file_type}"
    await message.photo[-1].download(destination_file=filename)
    effect = await state.get_data()
    is_filter = False if effect['effect'] == 'L' else True
    img = await make_filter_image(filename, effect['effect'], is_filter)
    await message.answer_photo(InputFile(img))
    await state.finish()
    os.unlink(img)
    # os.remove(img)


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(bot_start_handler, commands=['start'])
    dp.register_message_handler(back_btn_handler, text='🔙 Ortga')
    dp.register_message_handler(show_effects_handler, text='🖼 Rasimga Joziba berish')
    dp.register_message_handler(show_statistika_handler, text='📊 Statistika')
    dp.register_message_handler(support_handler, text='👩‍💻 Biz bilan aloqa')
    dp.register_message_handler(support_message_state, state=UserStates.support_message, content_types=['text'])
    dp.register_message_handler(get_user_photo_state, state=UserStates.get_photo, content_types=['photo', 'text'])
    dp.register_message_handler(get_selected_effect_handler, content_types=['text'])


