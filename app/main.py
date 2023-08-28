from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import mysql.connector
from . import models
from .database import engine
from .routers import item, user, auth, vote, filter
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["https://www.google.fi"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(item.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(filter.router)
