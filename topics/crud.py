from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from utils import get_ordering
from . import models, schemas


async def create_topic(db: AsyncSession, topic: schemas.TopicCreate):
    query = insert(models.DBTopic).values(
        name=topic.name,
        description=topic.description
    )
    result = await db.execute(query)
    await db.commit()
    response = {**topic.model_dump(), "id": result.lastrowid}
    return response


async def get_topic_by_id(db: AsyncSession, topic_id: int):
    query = select(models.DBTopic).where(models.DBTopic.id == topic_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_all_topics(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "name",
        order: str = "asc",
):
    ordering = get_ordering(models.DBTopic, sort_by, order)

    query = (
        select(models.DBTopic)
        .order_by(ordering)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_topic_by_name(db: AsyncSession, name: str):
    query = select(models.DBTopic).where(models.DBTopic.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_topic(
        db: AsyncSession,
        topic: schemas.Topic,
        topic_id: int
):
    db_topic = await get_topic_by_id(db, topic_id)

    if not db_topic:
        return None

    db_topic.name = topic.name
    db_topic.description = topic.description
    await db.commit()
    await db.refresh(db_topic)
    return db_topic


async def delete_topic(db: AsyncSession, topic_id: int):
    db_topic = await get_topic_by_id(db, topic_id)

    if not db_topic:
        return None

    await db.delete(db_topic)
    await db.commit()
    return db_topic
