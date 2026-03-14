import os
import redis


r = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)

def get_cached_link(code):

    return r.get(code)


def cache_link(code, url):

    r.set(code, url)


def delete_cached(code):

    r.delete(code)
