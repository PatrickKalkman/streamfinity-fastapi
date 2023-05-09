import uvicorn
from fastapi import FastAPI
from streamfinity_fastapi.routers import actors, movies, subscriptions, token, users
from sqlmodel import SQLModel
from streamfinity_fastapi.db import engine

app = FastAPI(title="Streamfinity API", version="0.1.0")
app.include_router(movies.router)
app.include_router(actors.router)
app.include_router(subscriptions.router)
app.include_router(users.router)
app.include_router(token.router)


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app, reload=True)
