import os
import subprocess
import time
from tqdm import tqdm
from config import DUMP_PAGE_VIEWS, DUMP_PAGE_VIEWS_DIR
from collections import Counter
from calendar import monthrange
from datetime import datetime, timedelta

GET_URL = (
    lambda timestamp: f"https://dumps.wikimedia.org/other/pageviews/{timestamp.year}/{timestamp.year}-{timestamp.month:02d}/{GET_FILE_NAME(timestamp)}.gz"
)
GET_FILE_NAME = (
    lambda timestamp: f"pageviews-{timestamp.year}{timestamp.month:02d}{timestamp.day:02d}-{timestamp.hour:02d}0000"
)
GET_ZIPPED_FILE_NAME = (
    lambda timestamp: f"{GET_FILE_NAME(timestamp)}.gz"
)

DOWNLOAD_BATCH_SIZE = 10

START_DATE = datetime(2021, 11, 1)
END_DATE = datetime(2022, 11, 1)
YEAR = 2021
MONTHS = 12
DAY_STEP = 4
HOURS_PER_DAY = 24
HOUR_STEP = 4


def get_timestamps_to_process():
    timestamps = []

    curr_date = START_DATE

    while curr_date < END_DATE:
        for h in range(0, HOURS_PER_DAY, HOUR_STEP):
            timestamps.append(datetime(curr_date.year, curr_date.month, curr_date.day, h))
        
        curr_date += timedelta(days=DAY_STEP)

    return timestamps


def timestamp_needs_download(timestamp):
    file_name = GET_FILE_NAME(timestamp)
    return not os.path.isfile(os.path.join(DUMP_PAGE_VIEWS_DIR, file_name))


def download_page_views(timestamps):
    undownloaded_timestamps = list(filter(timestamp_needs_download, timestamps))

    print(
        "Downloading timestamps",
        "Total:",
        len(timestamps),
        "Downloading:",
        len(undownloaded_timestamps)
    )

    print("\n".join([ timestamp.strftime("%m/%d/%Y, %H:%M:%S") for timestamp in undownloaded_timestamps ]))

    for timestamp in tqdm(undownloaded_timestamps):
        url = GET_URL(timestamp)
        command(["wget", url], DUMP_PAGE_VIEWS_DIR)

        zipped_file = GET_ZIPPED_FILE_NAME(timestamp)
        command(["gzip", "-d", zipped_file], DUMP_PAGE_VIEWS_DIR)


def parse_page_views(timestamp):
    file_name = GET_FILE_NAME(timestamp)

    with open(os.path.join(DUMP_PAGE_VIEWS_DIR, file_name), "r") as file:
        lines = file.read().splitlines()
        lines = filter(lambda line: line.startswith("en"), lines)
        lines = [line.split(" ") for line in lines]
        lines = filter(lambda line: len(line) >= 3, lines)
        page_views = {line[1]: int(line[2]) for line in lines}

    return Counter(page_views)


def command(command, cwd):
    return subprocess.run(
        command,
        cwd=cwd,
        shell=False,
    )


def main():
    if not os.path.exists(DUMP_PAGE_VIEWS_DIR):
        os.makedirs(DUMP_PAGE_VIEWS_DIR)

    start_time = time.time()

    timestamps = get_timestamps_to_process()
    download_page_views(timestamps)
    page_views = Counter()

    for timestamp in tqdm(timestamps):
        page_views.update(parse_page_views(timestamp))

    with open(DUMP_PAGE_VIEWS, "w+") as file:
        file.write(
            "\n".join(
                list(map(lambda item: item[0] + " " + str(item[1]), page_views.items()))
            )
        )

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
