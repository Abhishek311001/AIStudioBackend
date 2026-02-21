from fastapi import APIRouter, Depends
from dependencies import get_redis_conn, get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/health/redis")
async def health_redis(r=Depends(get_redis_conn)):
    return {"status": "ok", "service": "redis"}


@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "service": "postgres"}
