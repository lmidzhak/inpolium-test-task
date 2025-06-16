from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from posts import models, schemas
from utils import get_ordering


async def create_post(
        db: AsyncSession,
        post: schemas.PostCreate
):
    db_post = models.DBPost(
        topic_id=post.topic_id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def get_all_posts(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "title",
        order: str = "asc",
):
    ordering = get_ordering(models.DBPost, sort_by, order)

    query = (
        select(models.DBPost)
        .order_by(ordering)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_post_by_title(db: AsyncSession, title: str):
    query = select(models.DBPost).where(models.DBPost.title == title)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_post_by_id(db: AsyncSession, post_id: int):
    query = select(models.DBPost).where(models.DBPost.id == post_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_post(
        db: AsyncSession,
        post: schemas.PostUpdate,
        post_id: int
):
    query = select(models.DBPost).where(models.DBPost.id == post_id)
    result = await db.execute(query)
    db_post = result.scalar_one_or_none()

    if not db_post:
        return None
    db_post.title = post.title
    db_post.content = post.content
    db_post.topic_id = post.topic_id
    db_post.updated_at = post.updated_at
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, post_id: int):
    query = select(models.DBPost).where(models.DBPost.id == post_id)
    result = await db.execute(query)
    db_post = result.scalar_one_or_none()
    if not db_post:
        return None
    await db.delete(db_post)
    await db.commit()
    return db_post
