from config import TITLE_FILTERED, CLUE_TOKEN_FILTERED
from cnb_wiki_dictionary.download.caches import SummariesCache
from .clue_tokens_extractor import extract_clue_tokens

import json
from tqdm import tqdm


def main():
    with open(TITLE_FILTERED, "r") as file:
        titles = file.read().splitlines()

    summaries_cache = SummariesCache()
    title_to_summary = summaries_cache.get_key_to_value()
    title_clue_tokens = dict()

    for title in tqdm(titles):
        if title not in title_to_summary:
            continue
        clue_tokens = extract_clue_tokens(title, title_to_summary[title])
        if len(clue_tokens) > 0:
            title_clue_tokens[title] = clue_tokens

    with open(CLUE_TOKEN_FILTERED, "w+") as file:
        file.write(
            json.dumps(title_clue_tokens, indent=4, sort_keys=True, ensure_ascii=False)
        )


if __name__ == "__main__":
    main()
