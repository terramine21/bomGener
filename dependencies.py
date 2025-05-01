from db.session import get_session
from sqlmodel import Session
from fastapi import Request

# Глобальный счетчик запросов
request_counter = 0

def get_request_counter(request: Request):
    global request_counter
    request_counter += 1
    return request_counter