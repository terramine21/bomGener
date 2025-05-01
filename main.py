from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas #, crud
from db.database import SessionLocal, engine
from .services import bom_parser, pe3_generator
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



