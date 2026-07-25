from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from stark.core.database import get_db

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/database")
def database_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }
