import nest_asyncio
import asyncio
import logging
import aiosqlite
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
import quiz_data as qd
import db_commands as dbc

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)
DB_NAME = 'skyrim_quiz.db'
API_TOKEN = '6784969389:AAEEZ0zQO9Xfo_ba-hPNPeEu0VvCvB1HaVs'

bot = Bot(API_TOKEN,
          default=DefaultBotProperties(
              parse_mode="HTML"
          ))

dp = Dispatcher()

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer"))
    builder.adjust(1)
    return builder.as_markup()

right_answers_count = {}

@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = qd.quiz_data[current_question_index]['correct_option']
    await callback.message.answer(f"Ваш ответ <b>{qd.quiz_data[current_question_index]['options'][correct_option]}</b> правильный!")
    current_question_index += 1
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    results = right_answers_count.get(callback.from_user.id, 0)
    if user_id not in right_answers_count:
        right_answers_count[user_id] = 0
    right_answers_count[user_id] += 1

    await update_quiz_index(callback.from_user.id, current_question_index)
    if current_question_index < len(qd.quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен! Количество правильных ответов для пользователя {callback.from_user.full_name} - {right_answers_count.get(callback.from_user.id, 0)}")
        await save_results(user_id, user_name, results)

@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = qd.quiz_data[current_question_index]['correct_option']
    await callback.message.answer(f"Неправильно. Правильный ответ: {qd.quiz_data[current_question_index]['options'][correct_option]}")
    current_question_index += 1
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    results = right_answers_count.get(callback.from_user.id, 0)
    await update_quiz_index(user_id, current_question_index)
    if current_question_index < len(qd.quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен! Количество правильных ответов для пользователя {callback.from_user.full_name} - {results}")
        await save_results(user_id, user_name, results)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer(f"Добро пожаловать в квиз, <b>{message.from_user.full_name}</b>! Нажмите кнопку внизу, чтобы начать, или введите /whiterun !", 
                        parse_mode="HTML", 
                        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()
                 
async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = qd.quiz_data[current_question_index]['correct_option']
    opts = qd.quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{qd.quiz_data[current_question_index]['question']}", reply_markup=kb)

async def save_results(user_id, user_name, correct_answers):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO quiz_results (user_id, username, results) VALUES (?, ?, ?)', (user_id, user_name, correct_answers))
        await db.commit()

async def get_quiz_index(user_id):
     async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

@dp.message(F.text=="Начать игру")
@dp.message(Command("whiterun"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давай начнём!")
    await new_quiz(message)
    
async def main():

    await dbc.create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())