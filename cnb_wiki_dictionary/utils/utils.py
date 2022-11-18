import math

IGNORE_TOKENS = ["the", "of"]
SPLIT_CHARS = ["_", "-", "\u2013"]

MIN_VIEWS = 1e5
MAX_VIEWS = 1e7


def title_to_text(title):
    if "_(" in title:
        pieces = title.split("_(")
        title = pieces[0]
    return title.replace("_", " ")


def get_title_tokens(title):
    if "_(" in title:
        pieces = title.split("_(")
        title = pieces[0]
        # labels = pieces[1:]
        # Trim closing parentheses from label
        # labels = [label[:-1] for label in labels]

    for split_char in SPLIT_CHARS:
        title = title.replace(split_char, " ")
    tokens = title.split(" ")
    tokens = [token for token in tokens if token.lower() not in IGNORE_TOKENS]
    return tokens


def views_to_knownness(views):
    # Logarithmic interpolation so that max = 1 and min = 0
    # Caps at 1
    return min(math.log(views / MIN_VIEWS, 10) / math.log(MAX_VIEWS / MIN_VIEWS, 10), 1)
