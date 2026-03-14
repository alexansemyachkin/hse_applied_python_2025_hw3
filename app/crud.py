from sqlalchemy.orm import Session
from datetime import datetime

from . import models
from .utils import generate_short_code


def create_link(db: Session, original_url: str, custom_alias=None, expires_at=None):

    if custom_alias:
        existing = db.query(models.Link).filter(
            models.Link.short_code == custom_alias
        ).first()

        if existing:
            raise ValueError("alias already exists")

        code = custom_alias
    else:
        code = generate_short_code()

    link = models.Link(
        original_url=original_url,
        short_code=code,
        expires_at=expires_at
    )

    db.add(link)
    db.commit()
    db.refresh(link)

    return link


def get_link(db: Session, short_code: str):

    return db.query(models.Link).filter(
        models.Link.short_code == short_code
    ).first()


def delete_link(db: Session, short_code: str):

    link = get_link(db, short_code)

    if link:
        db.delete(link)
        db.commit()

    return link


def update_link(db: Session, short_code: str, new_url: str):

    link = get_link(db, short_code)

    if link:
        link.original_url = new_url
        db.commit()
        db.refresh(link)

    return link


def increment_click(db: Session, link):

    link.click_count += 1
    link.last_used_at = datetime.utcnow()

    db.commit()


def create_user(db: Session, email: str, password_hash: str):

    user = models.User(
        email=email,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def find_by_original_url(db: Session, original_url: str):

    return db.query(models.Link).filter(
        models.Link.original_url == original_url
    ).all()


def get_all_links(db: Session):

    return db.query(models.Link).all()


def get_top_links(db: Session):

    return db.query(models.Link)\
        .order_by(models.Link.click_count.desc())\
        .limit(10)\
        .all()
