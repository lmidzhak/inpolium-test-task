from contextlib import asynccontextmanager
from topics.models import DBTopic
from posts.models import DBPost
from comments.models import DBComment
from fastapi import FastAPI
from topics.router import router as topic_router
from posts.router import router as posts_router
from comments.router import router as comments_router

from database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(topic_router)
app.include_router(posts_router)
app.include_router(comments_router)


@app.get("/")
async def read_root():
    return {"message": "Hello, Blog management system!"}
