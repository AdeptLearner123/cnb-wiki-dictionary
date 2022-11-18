from cnb_wiki_dictionary.download.caches import SummariesCache
from cnb_wiki_dictionary.download.api_downloader import download
from config import TITLE_FILTERED, MISSING_SUMMARIES

from urllib.parse import quote_plus
from argparse import ArgumentParser
import os.path

GET_URL = (
    lambda page_title: f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(page_title)}"
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
        with open(MISSING_SUMMARIES, "a+") as file:
            file.write(key + "\n")
        return None, True

    if result.status_code != 200:
        print("Invalid status code", key, result.text)
        return None, False

    json = result.json()
    return json["extract"], True


def main():
    with open(TITLE_FILTERED, "r") as file:
        titles = file.read().splitlines()

    if os.path.isfile(MISSING_SUMMARIES):
        with open(MISSING_SUMMARIES, "r") as file:
            missing_summaries = set(file.read().splitlines())
            titles = [title for title in titles if title not in missing_summaries]

    email = parse_args()

    download(
        keys=titles,
        get_request_params=lambda title: get_request_params(title, email),
        cache=SummariesCache(),
        process_result=process_result,
        chunk_size=20,
        download_rate=50,
    )


if __name__ == "__main__":
    main()
