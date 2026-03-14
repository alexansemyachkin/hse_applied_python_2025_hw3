from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas
from ..services import cache


router = APIRouter(prefix="/links")


@router.post("/shorten", response_model=schemas.LinkResponse)
def shorten_link(data: schemas.LinkCreate, db: Session = Depends(get_db)):

    try:
        link = crud.create_link(
            db,
            data.original_url,
            data.custom_alias,
            data.expires_at
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="alias exists")

    return {"short_url": f"http://localhost:8000/{link.short_code}"}


@router.get("/{short_code}/stats", response_model=schemas.LinkStats)
def stats(short_code: str, db: Session = Depends(get_db)):

    link = crud.get_link(db, short_code)

    if not link:
        raise HTTPException(status_code=404)

    return link


@router.delete("/{short_code}")
def delete(short_code: str, db: Session = Depends(get_db)):

    link = crud.delete_link(db, short_code)

    if not link:
        raise HTTPException(status_code=404)

    cache.delete_cached(short_code)

    return {"status": "deleted"}


@router.put("/{short_code}")
def update(short_code: str, new_url: str, db: Session = Depends(get_db)):

    link = crud.update_link(db, short_code, new_url)

    if not link:
        raise HTTPException(status_code=404)

    cache.delete_cached(short_code)

    return {"status": "updated"}


@router.get("/search")
def search(original_url: str, db: Session = Depends(get_db)):

    links = crud.find_by_original_url(db, original_url)

    return links


@router.get("/")
def list_links(db: Session = Depends(get_db)):

    return crud.get_all_links(db)


@router.get("/top")
def top_links(db: Session = Depends(get_db)):

    return crud.get_top_links(db)
