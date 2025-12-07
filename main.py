import asyncio
from gc import callbacks

import requests
from aiogram import types,Bot,Dispatcher,F
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove

import os
load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
WEATHER_TOKEN=os.getenv('weather_token')
bot=Bot(token=BOT_TOKEN)
db=Dispatcher(bot=bot)


lokation_button=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='joylashuvni yuborish',request_location=True)
        ]
    ],
    resize_keyboard=True
)


category_buttons=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='hazirgi ob havo pragnozi',callback_data="hozirgi"),
            # InlineKeyboardButton(text='shu hafta ob havo pragnozi', callback_data='hafta'),
        ]
    ]
)




@db.message(Command('start'))
async def start_handler(message:types.Message):
    await message.answer('salom ob havoni bilish uchun bosing ⬇️',reply_markup=category_buttons)

@db.message(Command('help'))
async def start_handler(message:types.Message):
    await message.answer('salom ob havoni bilish uchun bosing ⬇️',reply_markup=category_buttons)


@db.callback_query(F.data=='hozirgi')
async def hozirgi_button(cal:types.CallbackQuery):
    await cal.message.answer('botni ishlatish uchun lokatsiyani yuboring',reply_markup=lokation_button)
    # res=requests.get('')
    # await cal.message.from_user.
    # await cal.message.answer()


@db.callback_query(F.data=='hafta')
async def haftalig_button(cal: types.CallbackQuery):
    url=f"https://api.openweathermap.org/data/2.5/forecast?lat=40.39&lon=71.48&units=metric&appid={WEATHER_TOKEN}"
    # url = f'https://api.openweathermap.org/data/2.5/onecall?lat=40.390929&lon=71.482167&exclude=minutely,hourly&units=metric&appid={WEATHER_TOKEN}'
    res = requests.get(url)
    data = res.json()
    await cal.message.answer(f'{data}')




@db.message(F.location)
async def locations(cal:types.Message):
    lat = cal.location.latitude
    lon = cal.location.longitude
    # url=f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=daily&appid={WEATHER_TOKEN}"
    # url=f"https://api.openweathermap.org/data/2.5/weather?q=Tashkent&appid={WEATHER_TOKEN}&units=metric"
    url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=metric"

    res=requests.get(url)
    data=res.json()

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    city = data["name"]

    text = (
        f"Manzil: {city}\n"
        f"Holati: {desc}\n\n"
        f"Harorat: {temp}°C<\n"
        f"His qilinadi: {feels}°C\n"
        f"Namlik: {humidity}%\n"
        f"Shamol tezligi: {wind} m/s\n"
    )
    await cal.answer(
        f"Manzil: {city}\n"
        f"Holati: {desc}\n\n"
        f"Harorat: {temp}°C\n"
        f"His qilinadi: {feels}°C\n"
        f"Namlik: {humidity}%\n"
        f"Shamol tezligi: {wind} m/s\n"
        f"qayta boshlash uchun=> /start",reply_markup=ReplyKeyboardRemove()
    )



# @db.message(Command('restartnow'))
# async def restartnow(message:types.Message):
#     global lat, lon
#     # lat = message.location.latitude
#     # lon = message.location.longitude
#     # url=f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=daily&appid={WEATHER_TOKEN}"
#     # url=f"https://api.openweathermap.org/data/2.5/weather?q=Tashkent&appid={WEATHER_TOKEN}&units=metric"
#     url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=metric"
#
#     res = requests.get(url)
#     data = res.json()
#
#     temp = data["main"]["temp"]
#     feels = data["main"]["feels_like"]
#     desc = data["weather"][0]["description"]
#     wind = data["wind"]["speed"]
#     humidity = data["main"]["humidity"]
#     city = data["name"]
#
#     text = (
#         f"Manzil: {city}\n"
#         f"Holati: {desc}\n\n"
#         f"Harorat: {temp}°C<\n"
#         f"His qilinadi: {feels}°C\n"
#         f"Namlik: {humidity}%\n"
#         f"Shamol tezligi: {wind} m/s\n"
#     )
#     await message.answer(
#         f"Manzil: {city}\n"
#         f"Holati: {desc}\n\n"
#         f"Harorat: {temp}°C\n"
#         f"His qilinadi: {feels}°C\n"
#         f"Namlik: {humidity}%\n"
#         f"Shamol tezligi: {wind} m/s\n"
#         f"qayta tekshirish uchun /restartnow"
#     )


async def main():
    print('bot ishga tushdi ....')
    await db.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())