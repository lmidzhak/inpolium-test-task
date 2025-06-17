from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, verify_token
from topics import schemas, crud

router = APIRouter(
    prefix="/topics",
    tags=["topics"],
    dependencies=[Depends(verify_token)]
)


@router.post(
    "/",
    response_model=schemas.Topic,
    summary="Create new topic"
)
async def add_topic(
        topic: schemas.TopicCreate,
        db: AsyncSession = Depends(get_db)
):
    db_topic = await crud.get_topic_by_name(db=db, name=topic.name)
    if db_topic:
        raise HTTPException(
            status_code=400, detail="Topic already exists"
        )
    return await crud.create_topic(db=db, topic=topic)


@router.get(
    "/",
    response_model=list[schemas.Topic],
    summary="Get a list of all topics",
)
async def topics_list(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=50),
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_topics(db=db, skip=skip, limit=limit)


@router.get(
    "/{topic_id}",
    response_model=schemas.Topic,
    summary="Get a topic by id",
)
async def read_topic(topic_id: int, db: AsyncSession = Depends(get_db)):
    topic = await crud.get_topic_by_id(db=db, topic_id=topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put(
    "/{topic_id}",
    response_model=schemas.Topic,
    summary="Update a topic info",
)
async def update_topic(
        topic_id: int,
        topic_data: schemas.Topic,
        db: AsyncSession = Depends(get_db)
):
    existing_topic = await crud.get_topic_by_id(db=db, topic_id=topic_id)
    if not existing_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if topic_data.name != existing_topic.name:
        topic_with_same_name = await crud.get_topic_by_name(
            db=db, name=topic_data.name
        )
        if topic_with_same_name:
            raise HTTPException(
                status_code=400, detail="Topic with this name already exists"
            )
    updated_topic = await crud.update_topic(
        db=db, topic_id=topic_id, topic=topic_data
    )
    return updated_topic


@router.delete(
    "/{topic_id}",
    response_model=schemas.Topic,
    summary="Delete topic from database"
)
async def delete_topic(topic_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_topic(db=db, topic_id=topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")
    return success
