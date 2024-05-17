import aiosqlite


async def authenticate_user(username, password):
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = await cursor.fetchone()
        return user is not None