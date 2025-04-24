import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from api import chat

app = FastAPI()

app.include_router(chat.router)
