
import requests
import json
import time

# API URLs
WIKIPEDIA_URL = "https://en.wikipedia.org/w/api.php"
OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

# Identify this project to the APIs
HEADERS = {
    "User-Agent": (
        "IS310CultureProject/1.0 "
        "(https://github.com/AnikaParade/is310-coding-assignments)"
    )
}


def get_api_data(url, params, api_name):
    """Request API data and handle errors."""

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=20
        )

        # Check the HTTP status before parsing JSON
        if response.status_code != 200:
            print(f"{api_name} error: HTTP {response.status_code}")
            return None

        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"{api_name} request failed: {error}")
        return None

    except ValueError:
        print(f"{api_name} returned invalid JSON.")
        return None


# -----------------------------------------
# API 1: MEDIAWIKI ACTION API
# -----------------------------------------

print("\n========== MEDIAWIKI API ==========")

wiki_params = {
    "action": "query",
    "format": "json",
    "prop": "extracts|info",
    "exintro": True,
    "explaintext": True,
    "inprop": "url",
    "titles": "Rapunzel"
}

wiki_response = get_api_data(
    WIKIPEDIA_URL,
    wiki_params,
    "MediaWiki"
)

wiki_item = None

if wiki_response:
    pages = wiki_response.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), None)

    if page and "missing" not in page:
        wiki_item = {
            "title": page.get("title"),
            "page_url": page.get("fullurl"),
            "extract": page.get("extract")
        }

        print(json.dumps(wiki_item, indent=4))
    else:
        print("The Rapunzel Wikipedia article was not found.")


# -----------------------------------------
# API 2: OPEN LIBRARY API
# -----------------------------------------

print("\n========== OPEN LIBRARY API ==========")

time.sleep(1)

library_params = {
    "title": "Rapunzel",
    "limit": 5,
    "fields": "key,title,author_name,first_publish_year,edition_count"
}

library_response = get_api_data(
    OPEN_LIBRARY_URL,
    library_params,
    "Open Library"
)

book_items = []
selected_book = None

if library_response:
    for book in library_response.get("docs", []):
        book_item = {
            "title": book.get("title"),
            "authors": book.get("author_name", []),
            "first_publish_year": book.get("first_publish_year"),
            "edition_count": book.get("edition_count"),
            "open_library_key": book.get("key")
        }

        book_items.append(book_item)

    print(json.dumps(book_items, indent=4))

    if book_items:
        selected_book = book_items[0]


# -----------------------------------------
# CONNECT THE TWO APIS
# -----------------------------------------

print("\n========== API CONNECTION ==========")

wiki_book_matches = []

if selected_book and selected_book.get("title"):

    time.sleep(1)

    book_title = selected_book["title"]

    print(f"Searching Wikipedia for: {book_title}")

    match_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": book_title,
        "srlimit": 5
    }

    match_response = get_api_data(
        WIKIPEDIA_URL,
        match_params,
        "Wikipedia book lookup"
    )

    if match_response:
        results = match_response.get(
            "query", {}
        ).get("search", [])

        for result in results:
            wiki_book_matches.append({
                "title": result.get("title"),
                "snippet": result.get("snippet"),
                "word_count": result.get("wordcount")
            })

        print(json.dumps(wiki_book_matches, indent=4))

        if wiki_book_matches:
            print("\nWikipedia returned possible matches.")
            print("These results still need to be checked for accuracy.")
        else:
            print("No matching Wikipedia articles were found.")

else:
    print("No Open Library book was available to look up.")


# -----------------------------------------
# SAVE SELECTED DATA AS JSON
# -----------------------------------------

saved_data = {
    "wikipedia_rapunzel": wiki_item,
    "open_library_books": book_items,
    "wikipedia_book_lookup": wiki_book_matches
}

with open(
    "rapunzel_open_library_data.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(saved_data, file, indent=4, ensure_ascii=False)

print("\n========== DATA SAVED ==========")
print("Saved to rapunzel_open_library_data.json")
