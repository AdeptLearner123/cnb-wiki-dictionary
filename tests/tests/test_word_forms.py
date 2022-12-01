import os
import json

from config import TESTS_DATA
from cnb_wiki_dictionary.utils.word_forms import get_word_forms
from cnb_wiki_dictionary.utils.spacy import make_doc
from cnb_wiki_dictionary.download.caches import SummariesCache


def test_clue_tokens_extractor():
    with open(os.path.join(TESTS_DATA, "word_forms.json")) as file:
        test_data = json.loads(file.read())

    summaries_cache = SummariesCache()

    for title, expected_word_forms in test_data.items():
        summary = summaries_cache.get_cached_value(title)
        expected_word_forms = set(expected_word_forms)
        doc = make_doc(summary)
        word_forms = set(get_word_forms(title, doc))
        assert (
            expected_word_forms == word_forms
        ), f"Expected {title} to have tokens {expected_word_forms} but was {word_forms}"
