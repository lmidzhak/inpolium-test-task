from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, verify_token
from posts import schemas, crud

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(verify_token)]
)


@router.post(
    "/",
    response_model=schemas.Post,
    summary="Create new post",
)
async def add_post(
        post: schemas.PostCreate,
        db: AsyncSession = Depends(get_db),
):
    db_post = await crud.get_post_by_title(db=db, title=post.title)
    if db_post:
        raise HTTPException(
            status_code=400, detail="This post title is already taken."
        )
    return await crud.create_post(db=db, post=post)


@router.get(
    "/",
    response_model=list[schemas.Post],
    summary="Get a list of all posts",
)
async def posts_list(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=50),
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_posts(db=db, skip=skip, limit=limit)


@router.get(
    "/{post_id}",
    response_model=schemas.Post,
    summary="Get a post by id",
)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_id(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail="Post not found"
        )
    return post


@router.put(
    "/{post_id}",
    response_model=schemas.Post,
    summary="Update post info"
)
async def update_post(
        post_id: int,
        post_data: schemas.PostUpdate,
        db: AsyncSession = Depends(get_db),
):
    post = await crud.get_post_by_id(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail="Post not found"
        )
    if post_data.title != post.title:
        post_with_same_title = await crud.get_post_by_title(
            db=db, title=post_data.title
        )

        if post_with_same_title:
            raise HTTPException(
                status_code=400, detail="This post title is already taken."
            )
    updated_post = await crud.update_post(
        db=db, post_id=post_id, post=post_data
    )
    return updated_post


@router.delete(
    "/{post_id}",
    response_model=schemas.Post,
    summary="Delete post from database"
)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_post(db=db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return success
