import asyncio
import os
from films import get_films, get_film_by_id
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
if not TOKEN or not API_KEY:
    raise ValueError("BOT_TOKEN или API_KEY не найдены в .env")
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
class Films(StatesGroup):
    title = State()
    choice = State()
@dp.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer('Введите название фильма (на английском)')
    await state.set_state(Films.title)
@dp.message(Films.title)
async def get_title(message: types.Message, state: FSMContext):
    title = message.text
    data = get_films(title, API_KEY)
    if data is None:
        await message.answer('Ошибка получения данных')
        await state.clear()
        return
    if not data or data.get("Response") == "False":
        await message.answer("Фильмы не найдены 😔")
        await state.clear()
        return
    films = data["Search"][:3]
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"{i+1}. {film['Title']}", callback_data=str(i))]
        for i, film in enumerate(films)
    ])
    await state.update_data(films=films)
    await state.set_state(Films.choice)
    await message.answer('Выбери фильм:', reply_markup=keyboard)
@dp.callback_query()
async def choose_film(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    films = data.get("films", [])
    index = int(call.data)
    if index < 0 or index >= len(films):
        await call.message.answer("Неверный выбор")
        await state.clear()
        return
    imdb_id = films[index]["imdbID"]
    film = get_film_by_id(imdb_id, API_KEY)
    if not film:
        await call.message.answer("Ошибка получения фильма")
        await state.clear()
        return
    text = (
        f"🎬 {film.get('Title')}\n"
        f"📅 {film.get('Year')}\n"
        f"⭐ {film.get('imdbRating')}\n\n"
        f"📖 {film.get('Plot')}"
    )

    poster = film.get("Poster")
    if poster and poster != "N/A":
        await call.message.answer_photo(photo=poster, caption=text)
    else:
        await call.message.answer(text)

    await call.answer()
    await state.clear()
async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())