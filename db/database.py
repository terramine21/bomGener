from sqlmodel import create_engine, Session, SQLModel
from config import settings
from models.models import DemoRecord

engine = create_engine(settings.DB_URL)

def init_db():

    SQLModel.metadata.create_all(engine)