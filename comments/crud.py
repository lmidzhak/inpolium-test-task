from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from comments import models, schemas
from utils import get_ordering


async def create_comment(
        db: AsyncSession,
        comment: schemas.CommentCreate,
):
    db_comment = models.DBComment(
        post_id=comment.post_id,
        text=comment.text,
        created_at=comment.created_at,
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_all_comments_by_post_id(
        db: AsyncSession,
        post_id: int,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = 'created_at',
        order: str = 'desc',
):
    ordering = get_ordering(models.DBComment, sort_by, order)

    query = (
        select(models.DBComment)
        .where(models.DBComment.post_id == post_id)
        .order_by(ordering)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_comment_by_id(db: AsyncSession, comment_id: int):
    query = select(models.DBComment).where(models.DBComment.id == comment_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_comment(
        db: AsyncSession,
        comment: schemas.CommentUpdate,
        comment_id: int
):
    db_comment = await get_comment_by_id(db=db, comment_id=comment_id)

    if not db_comment:
        return None

    db_comment.text = comment.text
    db_comment.post_id = comment.post_id
    db_comment.updated_at = comment.updated_at

    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def delete_comment(db: AsyncSession, comment_id: int):
    db_comment = await get_comment_by_id(db, comment_id)

    if not db_comment:
        return None

    await db.delete(db_comment)
    await db.commit()
    return db_comment
