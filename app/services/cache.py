import redis

r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


def get_cached_link(code):

    return r.get(code)


def cache_link(code, url):

    r.set(code, url)


def delete_cached(code):

    r.delete(code)
