from databases import Database
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_db():
    # Connect to the database
    await database.connect()

    # Create tables
    query1 = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );"""
    await database.execute(query=query1)

    # List of default users (username, password)
    default_users = [
        ("admin1", "hilarious_password"),
        ("anonymous1", "anonymous"),
        ("jwt_is_unbreakable1", "111111sdfeeeeg")  # Example admin user
    ]

    # Insert default users
    for username, password in default_users:
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        await database.execute(query=query, values={"username": username, "password": password})

    # Disconnect from the database
    await database.disconnect()

# Run the function to initialize the database
import asyncio
asyncio.run(init_db())