from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header, HTTPException, status

from database import SessionLocal
from dotenv import load_dotenv
import os

load_dotenv()


async def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {os.getenv('EXAMPLE_TOKEN')}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
