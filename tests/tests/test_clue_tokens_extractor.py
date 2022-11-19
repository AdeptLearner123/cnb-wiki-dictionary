import os
import json

from config import TESTS_DATA
from cnb_wiki_dictionary.clue_filter.clue_tokens_extractor import extract_clue_tokens
from cnb_wiki_dictionary.download.caches import SummariesCache


def test_clue_tokens_extractor():
    with open(os.path.join(TESTS_DATA, "clue_tokens_extractor.json")) as file:
        test_data = json.loads(file.read())

    summaries_cache = SummariesCache()

    for title, expected_tokens in test_data.items():
        summary = summaries_cache.get_cached_value(title)
        expected_tokens = set(expected_tokens)
        tokens = set(extract_clue_tokens(title, summary))
        assert (
            expected_tokens == tokens
        ), f"Expected {title} to have tokens {expected_tokens} but was {tokens}"
