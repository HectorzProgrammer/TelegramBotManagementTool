from sqlalchemy import Table, Column, Integer, String, Boolean
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("is_active", Boolean, default=True),
    Column("api_key", String, unique=True, index=True),
)
