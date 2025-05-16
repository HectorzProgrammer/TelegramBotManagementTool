import databases
import sqlalchemy

DATABASE_URL = "postgresql://username:password@localhost:5432/mydb"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# User Table
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True),
    sqlalchemy.Column("api_key", sqlalchemy.String, unique=True, index=True),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
