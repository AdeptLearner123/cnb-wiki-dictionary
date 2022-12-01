IGNORE_TOKENS = ["the", "of"]
SPLIT_CHARS = ["_", "-", "\u2013", ":"]


def title_to_text(title):
    if "_(" in title:
        pieces = title.split("_(")
        title = pieces[0]
    return title.replace("_", " ")


def tokenize(title):
    for split_char in SPLIT_CHARS:
        title = title.replace(split_char, " ")
    tokens = title.split(" ")
    return [ token.upper() for token in tokens if len(token) > 0]


def extract_title(title):
    if "_(" in title:
        pieces = title.split("_(")
        title = pieces[0]
    return title


def get_title_tokens(title):
    title = extract_title(title)
    tokens = tokenize(title)
    tokens = [token for token in tokens if token.lower() not in IGNORE_TOKENS]
    return tokens