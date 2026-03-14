from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .routers import links, auth
from .services import cache
from . import crud


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(links.router)
app.include_router(auth.router)


@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    cached = cache.get_cached_link(short_code)

    if cached:
        link = crud.get_link(db, short_code)
        if link:
            crud.increment_click(db, link)

        return RedirectResponse(cached)

    link = crud.get_link(db, short_code)

    if not link:
        raise HTTPException(status_code=404)

    crud.increment_click(db, link)

    cache.cache_link(short_code, link.original_url)

    return RedirectResponse(link.original_url)
