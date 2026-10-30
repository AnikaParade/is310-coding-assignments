
import requests
from urllib.robotparser import RobotFileParser

BASE_URL = "https://everafterhigh.miraheze.org"
ARTICLE = BASE_URL + "/wiki/Character_Biographies"
ROBOTS = BASE_URL + "/robots.txt"

HEADERS = {
    "User-Agent": "IS310-Student-Research/1.0 aparade2@illinois.edu"
}

# Test the article
try:
    response = requests.get(
        ARTICLE, headers=HEADERS, timeout=15
    )
    print("ARTICLE STATUS:", response.status_code)
    print("ARTICLE PREVIEW:", response.text[:300])
except requests.RequestException as e:
    print("ARTICLE ERROR:", e)

# Test robots.txt
try:
    response = requests.get(
        ROBOTS, headers=HEADERS, timeout=15
    )
    print("\nROBOTS STATUS:", response.status_code)
    print(response.text[:2000])

    if response.status_code == 200:
        parser = RobotFileParser()
        parser.parse(response.text.splitlines())

        print(
            "\nCAN SCRAPE ARTICLE:",
            parser.can_fetch(HEADERS["User-Agent"], ARTICLE)
        )
except requests.RequestException as e:
    print("ROBOTS ERROR:", e)
