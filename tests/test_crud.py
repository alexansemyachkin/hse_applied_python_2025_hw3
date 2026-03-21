from app import crud


def test_get_nonexistent(db_session):
    result = crud.get_link(db_session, "fake")
    assert result is None


def test_delete_nonexistent(db_session):
    result = crud.delete_link(db_session, "fake")
    assert result is None


def test_update_nonexistent(db_session):
    result = crud.update_link(db_session, "fake", "https://test.com")
    assert result is None
