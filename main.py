import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import CommandStart

TOKEN = "8354813359:AAGd6XctppfFNfOZkHJ2njUsrJJcYo5zenQ"

logging.basicConfig(level=logging.INFO)

def get_coordinates(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": "ru"
    }
    r = requests.get(url, params=params, timeout=10).json()
    if "results" not in r:
        return None
    city_data = r["results"][0]
    return (
        city_data["latitude"],
        city_data["longitude"],
        city_data["name"]
    )

def get_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    r = requests.get(url, params=params, timeout=10).json()
    return r["current_weather"]

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()


    @dp.message(Command(commands=["start"]))
    async def cmd_start(message: Message):
        await message.answer(
            "🌤 Бот прогноза погоды\n\n"
            "Напиши название города:\n"
            "Пример: Москва, Берлин, Париж"
        )

    @dp.message(F.text)
    async def weather(message: Message):
        city = message.text.strip()
        coords = get_coordinates(city)
        if not coords:
            await message.answer("❌ Город не найден")
            return
        lat, lon, city_name = coords
        weather = get_weather(lat, lon)
        temp = weather["temperature"]
        wind = weather["windspeed"]
        await message.answer(
            f"📍 {city_name}\n"
            f"🌡 Температура: {temp}°C\n"
            f"💨 Ветер: {wind} км/ч"
        )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
