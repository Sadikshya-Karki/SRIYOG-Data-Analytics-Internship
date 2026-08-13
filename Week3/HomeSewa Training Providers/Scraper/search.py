"""
search.py

Search helper using DDGS.

- Searches multiple queries
- Removes duplicate providers
- Prefers official websites
- Keeps Facebook only if no website exists
"""

import time
import random

from ddgs import DDGS
from urllib.parse import urlsplit, urlparse

from filters import is_bad_domain, is_social


SEARCH_PATTERNS = [

    "site:.np {}",

    "site:.com.np {}",

    "{} Kathmandu Nepal",

    "{} institute Kathmandu",

    "{} academy Nepal",

    "{} vocational training Nepal",

    "{} CTEVT Nepal",

    "{} course Kathmandu",

]


def generate_queries(service):

    return [pattern.format(service) for pattern in SEARCH_PATTERNS]


def clean_url(url):

    return urlsplit(url)._replace(
        query="",
        fragment=""
    ).geturl()


def get_domain(url):

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def search_service(service, max_results=10, delay_range=(4.0, 7.0)):

    providers = {}

    with DDGS(timeout=8) as ddgs:

        for query in generate_queries(service):

            print(f"Searching -> {query}")

            results = []

            for attempt in (1, 2):

                try:

                    results = list(
                        ddgs.text(
                            query,
                            max_results=max_results,
                            backend="bing"
                        )
                    )
                    break

                except Exception as e:

                    if attempt == 1:
                        print(f"Search failed (retrying once): {e}")
                        time.sleep(6)
                    else:
                        print(f"Search failed after retry: {e}")

            for result in results:

                url = (
                    result.get("href")
                    or result.get("link")
                )

                if not url:
                    continue

                url = clean_url(url)

                if is_bad_domain(url):
                    continue

                title = result.get("title", "").strip()

                domain = get_domain(url)

                social = is_social(url)

                # first time seeing this domain
                if domain not in providers:

                    providers[domain] = {

                        "title": title,

                        "url": url,

                        "body": result.get("body", ""),

                        "social": social,

                    }

                else:

                    existing = providers[domain]

                    # Prefer homepage over inner page
                    if len(url) < len(existing["url"]):

                        providers[domain] = {

                            "title": title,

                            "url": url,

                            "body": result.get("body", ""),

                            "social": social,

                        }

                    # Replace Facebook with official website
                    elif existing["social"] and not social:

                        providers[domain] = {

                            "title": title,

                            "url": url,

                            "body": result.get("body", ""),

                            "social": False,

                        }

            # Wait between queries so we don't get rate limited
            time.sleep(random.uniform(*delay_range))

    return [
        {
            "title": p["title"],
            "url": p["url"],
            "body": p["body"],
        }
        for p in providers.values()
    ]


def check_connection():
    """
    Quick smoke test: confirms DDGS can actually reach a backend
    before running the full 30-service pipeline. Run this first.
    """

    try:
        with DDGS(timeout=8) as ddgs:
            results = list(ddgs.text("test query", max_results=1, backend="bing"))
        if results:
            print("DDGS connection OK.")
            return True
        print("DDGS reached but returned no results.")
        return False
    except Exception as e:
        print(f"DDGS connection FAILED: {e}")
        return False


if __name__ == "__main__":

    print("Running connection check...")
    if not check_connection():
        print("Fix connectivity before running the full pipeline.")
    else:
        service = "plumbing training"

        results = search_service(service)

        print(f"\nFound {len(results)} providers\n")

        for i, result in enumerate(results, start=1):

            print(f"{i}. {result['title']}")
            print(result["url"])
            print()
