from config import DUMP_PAGE_VIEWS_FILTERED, TITLE_FILTERED

from .title_classifier import title_is_short_entity


def main():
    with open(DUMP_PAGE_VIEWS_FILTERED, "r") as file:
        titles = file.read().splitlines()

    filtered_titles = [title for title in titles if title_is_short_entity(title)]

    with open(TITLE_FILTERED, "w+") as file:
        file.write("\n".join(filtered_titles))


if __name__ == "__main__":
    main()
