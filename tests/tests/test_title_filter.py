import os
import json

from config import TESTS_DATA
from cnb_wiki_dictionary.title_filter.title_classifier import title_is_short_entity


def test_title_filter():
    with open(os.path.join(TESTS_DATA, "title_filter.json")) as file:
        test_data = json.loads(file.read())

    for title, label in test_data.items():
        assert (
            title_is_short_entity(title) == label
        ), f"Expected {title} to have label {label}"
