from .cache import Cache
from config import (
    PAGE_VIEWS_CACHE,
    SUMMARIES_CACHE,
)


class PageViewsCache(Cache):
    def __init__(self):
        super().__init__(PAGE_VIEWS_CACHE, True)


class SummariesCache(Cache):
    def __init__(self):
        super().__init__(SUMMARIES_CACHE, False)
