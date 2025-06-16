from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, verify_token
from comments import schemas, crud


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    # dependencies=[Depends(verify_token)]
)


@router.post(
    "/",
    response_model=schemas.Comment,
    summary="Create a new comment for specific post",
)
async def add_comment(
        comment: schemas.CommentCreate,
        db: AsyncSession = Depends(get_db),
):
    return await crud.create_comment(db=db, comment=comment)


@router.get(
    "/",
    response_model=list[schemas.Comment],
    summary="Get all comments for specific post",
)
async def comments_list_to_post(
        post_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=50),
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_comments_by_post_id(
        db=db, post_id=post_id, skip=skip, limit=limit
    )


@router.get(
    "/{comment_id}",
    response_model=schemas.Comment,
    summary="Get a specific comment",
)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await crud.get_comment_by_id(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=404, detail="Comment not found"
        )
    return comment


@router.put(
    "/{comment_id}",
    response_model=schemas.Comment,
    summary="Update a specific comment info",
)
async def update_comment(
        comment_id: int,
        comment_data: schemas.CommentUpdate,
        db: AsyncSession = Depends(get_db),
):
    updated_comment = await crud.update_comment(
        db=db, comment_id=comment_id, comment=comment_data
    )
    return updated_comment


@router.delete(
    "/{comment_id}",
    response_model=schemas.Comment,
    summary="Delete a specific comment",
)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_comment(db=db, comment_id=comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return success
