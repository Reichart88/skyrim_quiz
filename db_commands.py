import aiosqlite

async def create_table():
    async with aiosqlite.connect('skyrim_quiz.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER PRIMARY KEY, username TEXT, results INTEGER)''')
        await db.commit()

