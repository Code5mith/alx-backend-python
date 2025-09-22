import asyncio
import aiosqlite

async def async_fetch_users():
    """
    Asynchronously fetches all users from the database.
    """
    print("Starting async_fetch_all_users...")
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT name, age FROM users") as cursor:
            results = await cursor.fetchall()
            print("async_fetch_all_users finished.")
            return results

async def async_fetch_older_users():
    
    print("Starting async_fetch_older_users...")
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT name, age FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("async_fetch_older_users finished.")
            return results

async def fetch_concurrently():
    print("Running queries concurrently...")

    all_users, older_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    
    print("All users:", all_users)
    print("Users older than 40:", older_users)


asyncio.run(fetch_concurrently())
