import aiosqlite


async def create_db():
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY, telegram_id INT, username VARCHAR(30), password VARCHAR(50))''')
        await db.commit()
