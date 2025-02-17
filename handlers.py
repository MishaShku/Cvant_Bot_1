import random

from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router
import asyncio

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

agr = ""

user_router = Router()


emoji = ['🤯', '🤣', '✌️', '😂', '❤️']

class Reg(StatesGroup):
    name = State()
    agreement = State()
    password = State()
    number = State()


class Pull(StatesGroup):
    call = State()


@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Reg.agreement)
    await message.answer(text='Привет! Согласен ли ты на регистрацию?')


@user_router.message(Reg.agreement)
async def agreement(message: Message, state: FSMContext):
    global agr
    agr = message.text.lower()
    await state.update_data(agreement=message.text)
    if message.text.lower() == 'да':
        await message.answer(text='Отлично, тогда введи свое имя:')
    else:
        await message.answer(text='Окей, но мне нужно твое имя:')
    await state.set_state(Reg.name)


@user_router.message(Reg.name)
async def name(message: Message, state: FSMContext):
    global agr
    f = open('date.txt', 'a+')
    f.write(f'{message.text} ')
    await state.update_data(name=message.text)
    if agr == 'да':
        await message.answer(text=f'Рад познакомиться, {message.text}, придумай пароль:')
        await state.set_state(Reg.password)
        f.close()
    else:
        await message.answer(text=f'Все, гуляй, {message.text}')
        f.write('\n')
        await state.clear()
        f.close()


@user_router.message(Reg.password)
async def password(message: Message, state: FSMContext):
    f = open('date.txt', 'a+')
    f.write(f'{message.text}\n')
    f.close()
    await state.update_data(password=message.text)
    await message.answer(text='Хорошо, осталось указать свой номер телефона:')
    await state.set_state(Reg.number)


@user_router.message(Reg.number)
async def number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer(text='Регистрация успешно завершена, чтобы получить смайлик, введите команду "/pull"')
    await state.clear()


@user_router.message(Command('pull'))
async def number(message: Message, state: FSMContext):
    await state.set_state(Pull.call)
    await message.answer(text='Введите ваше имя пользователя и пароль через пробел:')


@user_router.message(Pull.call)
async def number(message: Message, state: FSMContext):
    global emoji
    f = open('date.txt', 'r')
    d = message.text.split()
    fl = False
    for i in f:
        if len(d) > 1:
            st = i.split()
            if d[0] == st[0] and d[1] == st[1]:
                fl = True
                break
    f.close()
    if fl:
        smile = random.randint(0, 4)
        await message.answer(text=f'{emoji[smile]}')
        await state.clear()
    else:
        await message.answer(text='Неверное имя пользователя или пароль, попробуйте ещё раз')
        await state.set_state(Pull.call)
