"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
from aiogram import Bot, Dispatcher, executor, types

import asyncio

from oxfordLookup import getDefinitions
from googletrans import Translator

translator = Translator()

API_TOKEN = 'Your Telegram bot API'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Assalomu alaykum  {message.from_user.first_name}, Men speaker bot man")
    # message.from_user.username >> bu foydalanuvchini usernameini chiqarib beradi misol uchun @abdulloh, @username....


@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    await message.reply('''
Menga 1 dona so'zni yuborsangiz men sizga yuborgan so'zingizni ingliz tilida qanday o'qilish kerakligini aytib beraman😊

Agar yuborgan so'zingiz 1 dona so'zdan ko'p bo'lsa ingliz tiliga tarjima qilib beraman agar ingliz tilida yozsangiz uzbek tiliga tarjima qilaman🙃
    ''')


@dp.message_handler()
async def tarjimon(message: types.Message):
    print(message)
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:

            await asyncio.sleep(1)
            await types.ChatActions.typing()

            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await asyncio.sleep(1)
                await types.ChatActions.record_voice()

                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
