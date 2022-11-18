import os
import json

from config import TESTS_DATA
from cnb_wiki_dictionary.clue_filter.clue_tokens_extractor import extract_clue_tokens
from cnb_wiki_dictionary.download.caches import SummariesCache


def test_variants_extractor():
    with open(os.path.join(TESTS_DATA, "variants_extractor.json")) as file:
        test_data = json.loads(file.read())

    summaries_cache = SummariesCache()

    for title, expected_variants in test_data.items():
        summary = summaries_cache.get_cached_value(title)
        expected_variants = set(expected_variants)
        variants = set(extract_clue_tokens(title, summary))
        assert (
            expected_variants == variants
        ), f"Expected {title} to have variants {expected_variants} but was {variants}"
