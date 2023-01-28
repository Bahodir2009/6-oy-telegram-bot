import asyncio
import logging
from aiogram import Dispatcher, Bot, executor, types

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = '5674925771:AAE-McW8QREcJ90gSsv2ivWPZEPDr2oEbEM'

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# start_menu_btn = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
# start_menu_btn.add(
#     types.KeyboardButton(text='Location'),
#     types.KeyboardButton(text='Quiz'),
#     types.KeyboardButton(text='emoji'),
#     types.KeyboardButton(text='sticker'),
# )

start_menu_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_menu_btn.row('📍 Location')
start_menu_btn.row('📚 Quiz', '❤️‍🔥 emoji')
start_menu_btn.row('🎉 sticker')


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command='start', description="Botni ishga tushurish"),
            types.BotCommand(command='help', description='Yordam olish'),
        ]
    )


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer("Assalomu aleykum", reply_markup=start_menu_btn)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_commands, skip_updates=True)