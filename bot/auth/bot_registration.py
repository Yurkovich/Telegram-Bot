import aiosqlite


async def register_user(username, password):
    async with aiosqlite.connect('users.db') as db:
        await db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        await db.commit()