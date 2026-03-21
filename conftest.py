import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.services import cache

engine = create_engine("sqlite:///./test.db")
TestingSessionLocal = sessionmaker(bind=engine)


class FakeCache:
    def __init__(self):
        self.storage = {}

    def get_cached_link(self, code):
        return self.storage.get(code)

    def cache_link(self, code, url):
        self.storage[code] = url

    def delete_cached(self, code):
        if code in self.storage:
            del self.storage[code]


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)

@pytest.fixture(autouse=True)
def override_cache():
    fake_cache = FakeCache()

    cache.get_cached_link = fake_cache.get_cached_link
    cache.cache_link = fake_cache.cache_link
    cache.delete_cached = fake_cache.delete_cached
