from sqlmodel import SQLModel, Session, create_engine
from os import environ as env


db_url = f"postgresql://{env["POSTGRES_USER"]}:{env["POSTGRES_PASSWORD"]}@db:5432/{env["POSTGRES_DB"]}"

engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# template is postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]