from fastapi import FastAPI
from connection import *
import uvicorn
from routes import router


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)