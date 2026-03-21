from app.services import cache

def test_cache_basic():
    cache.cache_link("abc", "url")
    assert cache.get_cached_link("abc") == "url"

    cache.delete_cached("abc")
    assert cache.get_cached_link("abc") is None
