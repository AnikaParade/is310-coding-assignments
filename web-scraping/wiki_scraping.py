
import requests
import time
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

# --------------------------------------------------
# PROJECT SETTINGS
# --------------------------------------------------

BASE_URL = "https://everafterhigh.miraheze.org"

START_URL = (
    BASE_URL + "/wiki/Character_Biographies"
)

ROBOTS_URL = BASE_URL + "/robots.txt"

# Replace with your actual Illinois NetID email.
HEADERS = {
    "User-Agent": (
        "IS310-EverAfterHigh-Research/1.0 "
        "(YOUR_NETID@illinois.edu)"
    )
}

DELAY = 5
MAX_ARTICLES = 20

OUTPUT_FILE = "ever_after_high_data.csv"

session = requests.Session()
session.headers.update(HEADERS)


# --------------------------------------------------
# STEP 1: CHECK ROBOTS.TXT
# --------------------------------------------------

def check_robots():
    print("Checking robots.txt...")

    try:
        response = session.get(
            ROBOTS_URL,
            timeout=15
        )

        print("Robots status:", response.status_code)

        if response.status_code != 200:
            print("Cannot verify robots.txt. Stopping.")
            return None

        parser = RobotFileParser()
        parser.set_url(ROBOTS_URL)
        parser.parse(response.text.splitlines())

        return parser

    except requests.RequestException as error:
        print("Robots error:", error)
        return None


# --------------------------------------------------
# STEP 2: DOWNLOAD AND PARSE A PAGE
# --------------------------------------------------

last_request_time = 0


def get_page(url, robots):
    global last_request_time

    # Check whether robots.txt allows this URL.
    if not robots.can_fetch(HEADERS["User-Agent"], url):
        print("Disallowed by robots.txt:", url)
        return None

    # Wait between requests.
    elapsed = time.time() - last_request_time

    if last_request_time > 0 and elapsed < DELAY:
        time.sleep(DELAY - elapsed)

    try:
        response = session.get(
            url,
            timeout=15
        )

        last_request_time = time.time()

        print(response.status_code, url)

        # Never parse unsuccessful responses.
        if response.status_code != 200:
            print("Skipping unsuccessful page.")
            return None

        preview = response.text[:1500].lower()

        if (
            "just a moment..." in preview
            or "enable javascript and cookies" in preview
        ):
            print("Access challenge detected. Stopping.")
            return None

        return BeautifulSoup(
            response.text,
            "html.parser"
        )

    except requests.RequestException as error:
        print("Request error:", error)
        return None


# --------------------------------------------------
# STEP 3: FIND CHARACTER ARTICLE LINKS
# --------------------------------------------------

def get_character_links(soup):
    links = {}

    content = soup.select_one(
        "div.mw-parser-output"
    )

    if content is None:
        print("Could not find the main article content.")
        return links

    excluded_namespaces = (
        "Special:",
        "Category:",
        "File:",
        "Help:",
        "Talk:",
        "User:",
        "Template:",
        "MediaWiki:",
        "Portal:",
    )

    for link in content.select("a[href]"):
        href = link.get("href", "")
        title = link.get_text(" ", strip=True)

        if not title:
            continue

        if not href.startswith("/wiki/"):
            continue

        page_name = href.split("/wiki/", 1)[-1]

        if page_name.startswith(excluded_namespaces):
            continue

        full_url = urljoin(BASE_URL, href)

        # Keep links on the Ever After High wiki only.
        if urlparse(full_url).netloc != urlparse(BASE_URL).netloc:
            continue

        links[full_url] = title

    return links


# --------------------------------------------------
# STEP 4: EXTRACT CHARACTER INFORMATION
# --------------------------------------------------

def get_infobox_value(soup, possible_labels):
    """
    Look for information in an article infobox.
    Field names vary, so unavailable values remain blank.
    """

    for row in soup.select("table.infobox tr"):
        header = row.find(["th", "td"])

        if header is None:
            continue

        label = header.get_text(" ", strip=True).lower()

        if any(
            possible_label in label
            for possible_label in possible_labels
        ):
            value_cells = row.find_all("td")

            if value_cells:
                return value_cells[-1].get_text(
                    " ", strip=True
                )

    return ""


def measure_article(url, title, page_type, source_page, robots):

    soup = get_page(url, robots)

    if soup is None:
        return None

    content = soup.select_one(
        "div.mw-parser-output"
    )

    if content is None:
        print("Main article content missing.")
        return None

    # Extract information before cleaning the article.
    origin = get_infobox_value(
        soup,
        ["origin", "based on", "fairy tale", "fairytale", "story"]
    )

    affiliation = get_infobox_value(
        soup,
        ["royal/rebel", "royal or rebel", "alignment", "affiliation"]
    )

    # Remove page elements that are not article text.
    for element in content.select(
        "script, style, .mw-editsection, .toc"
    ):
        element.decompose()

    article_text = content.get_text(
        " ",
        strip=True
    )

    # Count unique internal article links.
    internal_links = set()

    for link in content.select('a[href^="/wiki/"]'):
        href = link.get("href", "")

        if not href:
            continue

        page_name = href.split("/wiki/", 1)[-1]

        if page_name.startswith(
            ("Special:", "Category:", "File:", "Help:")
        ):
            continue

        internal_links.add(urljoin(BASE_URL, href))

    record = {
        "character_name": title,
        "url": url,
        "page_type": page_type,
        "discovered_from": source_page,
        "fairy_tale_origin": origin,
        "royal_or_rebel": affiliation,
        "word_count": len(article_text.split()),
        "character_count": len(article_text),
        "internal_link_count": len(internal_links),
    }

    return record


# --------------------------------------------------
# STEP 5: RUN THE SCRAPER
# --------------------------------------------------

def main():

    print("Starting Ever After High scraper...")

    robots = check_robots()

    if robots is None:
        print("Scraper stopped because robots.txt could not be checked.")
        return

    # First page type: character biography listing.
    index_soup = get_page(START_URL, robots)

    if index_soup is None:
        print("Could not access the biography listing.")
        return

    results = []

    # Record the listing page itself.
    index_record = measure_index(index_soup)

    results.append(index_record)

    # Second page type: individual character articles.
    character_links = get_character_links(index_soup)

    print(
        "Found",
        len(character_links),
        "candidate character links."
    )

    count = 0

    for url, title in character_links.items():

        if count >= MAX_ARTICLES:
            break

        print("\nCollecting:", title)

        record = measure_article(
            url,
            title,
            "character_article",
            START_URL,
            robots
        )

        if record is not None:
            results.append(record)
            count += 1

    # Save the results as CSV.
    if not results:
        print("No data was collected.")
        return

    fieldnames = [
        "character_name",
        "url",
        "page_type",
        "discovered_from",
        "fairy_tale_origin",
        "royal_or_rebel",
        "word_count",
        "character_count",
        "internal_link_count",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n--------------------------------")
    print("SCRAPING COMPLETE")
    print("--------------------------------")
    print("Pages saved:", len(results))
    print("Character articles:", count)
    print("Output file:", OUTPUT_FILE)


# --------------------------------------------------
# MEASURE THE STARTING LISTING PAGE
# --------------------------------------------------

def measure_index(soup):

    content = soup.select_one(
        "div.mw-parser-output"
    )

    if content is None:
        content = soup

    text = content.get_text(" ", strip=True)

    links = {
        urljoin(BASE_URL, link.get("href"))
        for link in content.select('a[href^="/wiki/"]')
    }

    return {
        "character_name": "Character Biographies",
        "url": START_URL,
        "page_type": "biography_listing",
        "discovered_from": "",
        "fairy_tale_origin": "",
        "royal_or_rebel": "",
        "word_count": len(text.split()),
        "character_count": len(text),
        "internal_link_count": len(links),
    }


if __name__ == "__main__":
    main()
