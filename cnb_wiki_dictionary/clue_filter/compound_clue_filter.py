from config import TITLE_FILTERED, COMPOUND_CLUE_FILTERED, CARDWORDS
from cnb_wiki_dictionary.utils.title import get_title_tokens

import json


def extract_compound_tokens(title):
    tokens = get_title_tokens(title)

    if len(tokens) != 2:
        return None

    return tokens


def main():
    with open(TITLE_FILTERED, "r") as file:
        titles = file.read().splitlines()

    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    compound_tokens = dict()

    for title in titles:
        tokens = extract_compound_tokens(title)

        if tokens is not None and any([token.upper() in cardwords for token in tokens]):
            compound_tokens[title] = tokens

    with open(COMPOUND_CLUE_FILTERED, "w+") as file:
        file.write(
            json.dumps(compound_tokens, indent=4, sort_keys=True, ensure_ascii=False)
        )


if __name__ == "__main__":
    main()
