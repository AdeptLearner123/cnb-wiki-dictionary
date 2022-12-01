import os
import json

from config import TESTS_DATA, DUMP_PAGE_VIEWS_FILTERED

def test_dump_page_views_filter():
    with open(os.path.join(TESTS_DATA, "dump_page_view_filter.json")) as file:
        expected_titles = json.loads(file.read())

    with open(DUMP_PAGE_VIEWS_FILTERED, "r") as file:
        filtered_titles = set(file.read().splitlines())

    for title in expected_titles:
        assert (
            title in filtered_titles
        ), f"Expected {title} to be in filtered titles"
