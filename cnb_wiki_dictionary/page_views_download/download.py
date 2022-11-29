from cnb_wiki_dictionary.download.caches import PageViewsCache
from cnb_wiki_dictionary.download.api_downloader import download
from config import CLUE_TOKEN_FILTERED, COMPOUND_CLUE_FILTERED, MISSING_PAGE_VIEWS

from urllib.parse import quote_plus
from argparse import ArgumentParser
import json
import os.path

GET_URL = (
    lambda page_title: f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{quote_plus(page_title)}/monthly/2021110100/2022110100"
)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--email", type=str, required=True)
    args = parser.parse_args()
    return args.email


def get_request_params(page_title, email):
    return {
        "url": GET_URL(page_title),
        "headers": {"User-Agent": f"CodeNamesBot/0.0 ({email}) python-requests/0.0"},
    }


def process_result(key, result):
    if result.status_code == 404:
        print("Not found", key)
        with open(MISSING_PAGE_VIEWS, "a") as file:
            file.write(key + "\n")
        return None, True

    if result.status_code != 200:
        print("Invalid status code", key, result.text)
        return None, False

    json = result.json()
    monthly_views = [item["views"] for item in json["items"]]
    
    if key == "Block,_Inc.":
        print("Json", json)
        print("Monthly views", monthly_views)
        print(sum(monthly_views))
    return sum(monthly_views), True


def main():
    titles = set()

    with open(CLUE_TOKEN_FILTERED, "r") as file:
        titles.update(json.loads(file.read()).keys())

    with open(COMPOUND_CLUE_FILTERED, "r") as file:
        titles.update(json.loads(file.read()).keys())

    if os.path.isfile(MISSING_PAGE_VIEWS):
        with open(MISSING_PAGE_VIEWS, "r") as file:
            missing_page_views = set(file.read().splitlines())
            titles = titles.difference(missing_page_views)

    email = parse_args()

    download(
        keys=titles,
        get_request_params=lambda title: get_request_params(title, email),
        cache=PageViewsCache(),
        process_result=process_result,
        chunk_size=20,
        download_rate=1.5,
    )


if __name__ == "__main__":
    main()
