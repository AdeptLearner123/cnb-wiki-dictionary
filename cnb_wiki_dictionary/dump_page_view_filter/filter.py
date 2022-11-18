from config import DUMP_PAGE_VIEWS, ALL_TITLES, DUMP_PAGE_VIEWS_FILTERED


PAGE_VIEW_THRESHOLD = 8000


def main():
    print("Status:", "Reading dump page views")
    with open(DUMP_PAGE_VIEWS, "r") as file:
        lines = file.read().splitlines()
        lines = [line.split(" ") for line in lines]
        page_views = {line[0]: int(line[1]) for line in lines}

    print("Status:", "Reading wiki page titles")
    with open(ALL_TITLES) as file:
        page_titles = file.read().splitlines()

    print("Status:", "Filtering by dump page views")
    filtered_titles = [
        title
        for title in page_titles
        if title in page_views and page_views[title] > PAGE_VIEW_THRESHOLD
    ]

    print("Status:", "Dumping")
    with open(DUMP_PAGE_VIEWS_FILTERED, "w+") as file:
        file.write("\n".join(filtered_titles))


if __name__ == "__main__":
    main()
