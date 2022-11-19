from cnb_wiki_dictionary.utils.title import get_title_tokens


def title_is_short_entity(title):
    if (
        title.startswith("List_of_")
        or title.startswith("History_of_")
        or "(disambiguation)" in title
    ):
        return False

    tokens = get_title_tokens(title)
    return len(tokens) <= 2
