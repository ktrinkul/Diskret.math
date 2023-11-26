from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from pydoc import html
from aiogram.types import ReplyKeyboardRemove

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import random
import json
from datetime import datetime
import asyncio

from config_reader import config
bot = Bot(token = config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher()
storage = MemoryStorage()

class FSMtrips(StatesGroup):
    get_classic_prose_for = State()

available_request = ['Стих дня', 'Классический стих', 'Современный стих', 'Спасибо, начитался']
available_prose = ["Дети", "Взрослые", "В меню"]

builder = ReplyKeyboardBuilder()
for i in range(2): builder.add(types.KeyboardButton(text=available_request[i]))
builder.adjust(2)
for i in range(2, 4): builder.add(types.KeyboardButton(text=available_request[i]))
builder.adjust(2)

@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        text = f'{message.from_user.full_name}! Что хотите почитать?',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    #await state.set_state(default_state)

def get_prose_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

@dp.message(F.text == "Стих дня", StateFilter(default_state))
async def send_prose(message: types.Message, state: FSMContext):
    day = datetime.today().day
    text = get_prose_from_json('prose_of_the_day.json')
    prose_text = text.get(str(day))
    await message.answer(prose_text)
    await state.clear()

@dp.message(F.text == "Современный стих", StateFilter(default_state))
async def send_prose(message: types.Message, state: FSMContext):
    text = get_prose_from_json('prose_modern.json')
    prose_text = text.get(str(random.randint(1, 5)))
    await message.answer(prose_text)
    await state.clear()

#смена состояния
@dp.message(F.text == "Классический стих", StateFilter(default_state))
async def choose_type_of_prose(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    for i in range(2): builder.add(types.KeyboardButton(text=available_prose[i]))
    builder.adjust(2)
    builder.add(types.KeyboardButton(text=available_prose[2]))
    builder.adjust(1)
    await message.answer(
        text = f'{message.from_user.full_name}, выберите для какого возраста должны быть преднозначены эти стихи',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(FSMtrips.get_classic_prose_for)

@dp.message(F.text == "Дети", FSMtrips.get_classic_prose_for)
async def send_place(message: types.Message, state: FSMContext):
    text = get_prose_from_json('prose_classic_child.json')
    prose_text = text.get(str(random.randint(1, 5)))
    await message.answer(prose_text)
    ###
    await message.answer(
        text='Хотите почитать еще?',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.clear()

@dp.message(F.text == "Взрослые", FSMtrips.get_classic_prose_for)
async def send_place(message: types.Message, state: FSMContext):
    text = get_prose_from_json('prose_classic_adult.json')
    prose_text = text.get(str(random.randint(1, 5)))
    await message.answer(prose_text)
    ###
    await message.answer(
        text='Хотите почитать еще?',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.clear()


#выход из различных состояний
@dp.message(StateFilter(default_state), Command("cancel"))
@dp.message(StateFilter(default_state), F.text == "Спасибо, начитался")
async def cmd_cancel_no_state(message: types.Message, state: FSMContext):
    #Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Если захотите почитать еще, нажмите команду /start",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dp.message(Command('cancel'), FSMtrips.get_classic_prose_for)
@dp.message(F.text == "В меню")
async def process_cancel_state(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    for i in range(2): builder.add(types.KeyboardButton(text=available_request[i]))
    builder.adjust(2)
    for i in range(2, 4): builder.add(types.KeyboardButton(text=available_request[i]))
    builder.adjust(2)
    await message.answer(
        text=f'Что хотите почитать?',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.clear()

@dp.message(Command('cancel'), ~StateFilter(default_state, FSMtrips.get_classic_prose_for))
@dp.message(F.text == "Спасибо, начитался")
async def process_cancel_state(message: types.Message, state: FSMContext):
    await message.answer(text='Возвращаемся в начало', reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


#неучитываемые вводы
@dp.message(StateFilter(default_state))
async def send_echo(message: types.Message):
    await message.answer('Извините, такой команды нет\n'
                         'Для возвращения в начало нажмите команду /start')

@dp.message(FSMtrips.get_classic_prose_for)
async def send_echo(message: types.Message):
    await message.answer('Извините, такой команды нет\n'
                         'Для продолжения отправьте одну из команд\n'
                         '-возвращение в начало /start\n'
                         '-отмена /cancel')

#подключение бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())