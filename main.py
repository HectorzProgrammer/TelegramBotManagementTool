from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import database
from schemas import UserCreate, UserOut, Token
from crud import create_user, authenticate_user
from auth import create_access_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için, sonradan domain kısıtla
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing_user = await authenticate_user(user.email, user.password)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email zaten kayıtlı")
    user_created = await create_user(user.email, user.password)
    return user_created

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email veya şifre yanlış")
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
