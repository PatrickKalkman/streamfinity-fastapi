import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from db import engine
from routers import movies, actors


app = FastAPI(title="Streamfinity API", version="0.1.0")
app.include_router(movies.router)
app.include_router(actors.router)


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app, reload=True)
