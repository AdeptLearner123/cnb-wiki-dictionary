from config import (
    COMPOUND_DICT,
    COMPOUND_CLUE_FILTERED,
    CLUE_TOKEN_FILTERED,
    CLUE_TOKEN_DICT,
)
from cnb_wiki_dictionary.download.caches import PageViewsCache, SummariesCache
from cnb_wiki_dictionary.utils.utils import title_to_text, views_to_knownness

import json


def main():
    create_dict(COMPOUND_CLUE_FILTERED, COMPOUND_DICT)
    create_dict(CLUE_TOKEN_FILTERED, CLUE_TOKEN_DICT)


def create_dict(TITLE_TOKENS_PATH, OUTPUT_PATH):
    with open(TITLE_TOKENS_PATH, "r") as file:
        title_tokens = json.loads(file.read())

    dictionary = dict()

    title_to_summary = SummariesCache().get_key_to_value()
    title_to_views = PageViewsCache().get_key_to_value()

    for title, tokens in title_tokens.items():
        if title not in title_to_summary or title not in title_to_views:
            continue

        knownness = views_to_knownness(title_to_views[title])

        if knownness < 0:
            continue

        dictionary[title] = {
            "word": title_to_text(title),
            "definition": title_to_summary[title],
            "knownness": knownness,
            "tokens": tokens,
        }

    with open(OUTPUT_PATH, "w+") as file:
        file.write(json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
