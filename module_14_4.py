from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb1.row(button1, button2)
kb1.row(button3)

kb2 = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
kb2.row(button1, button2)

kb3 = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb3.row(button1, button2, button3, button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет, {message.from_user.username}! Я бот, помогающий твоему здоровью.', reply_markup=kb1)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Этот бот поможет тебе рассчитать суточную норму калорий, '
                         'в зависимости от твоего возраста, роста и веса. \n Жми "РАССЧИТАТЬ"', reply_markup=kb1)


@dp.message_handler(text='Рассчитать')
async def inline_info(message):
    await message.answer('Выбери опцию: ', reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def formulas(call):
    await call.message.answer('Формула расчета нормы калорий: \n 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес в килограммах:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма калорий: {calories} ккал', reply_markup=kb1)
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    await message.answer(f'Название:{get_all_products()[0][0]} | Описание:{get_all_products()[0][1]} | Цена:{get_all_products()[0][2]}')
    with open('vit_C.jpeg', "rb") as img:
        await message.answer_photo(img)
    await message.answer(f'Название:{get_all_products()[1][0]} | Описание:{get_all_products()[1][1]} | Цена:{get_all_products()[1][2]}')
    with open('vit_D.jpg', "rb") as img:
        await message.answer_photo(img)
    await message.answer(f'Название:{get_all_products()[2][0]} | Описание:{get_all_products()[2][1]} | Цена:{get_all_products()[2][2]}')
    with open('vit_Mg.jpg', "rb") as img:
        await message.answer_photo(img)
    await message.answer(f'Название:{get_all_products()[3][0]} | Описание:{get_all_products()[3][1]} | Цена:{get_all_products()[3][2]}')
    with open('vit_Zn.png', "rb") as img:
        await message.answer_photo(img, reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)