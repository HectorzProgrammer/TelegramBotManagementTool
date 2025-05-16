import secrets
from database import users, database
from auth import hash_password, verify_password

async def create_user(email: str, password: str):
    hashed_password = hash_password(password)
    api_key = secrets.token_urlsafe(32)
    query = users.insert().values(email=email, hashed_password=hashed_password, api_key=api_key)
    await database.execute(query)
    return {"email": email, "api_key": api_key}

async def get_user_by_email(email: str):
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)

async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user
