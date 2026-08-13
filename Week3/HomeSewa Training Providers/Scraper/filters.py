"""
filters.py

Utilities for filtering search results and detecting Nepal-based websites.
"""

from urllib.parse import urlparse

# Websites that are NOT training providers
BAD_DOMAINS = {

    # Search engines
    "google.com",
    "bing.com",
    "duckduckgo.com",
    "search.yahoo.com",

    # Dictionaries
    "wikipedia.org",
    "wiktionary.org",
    "dictionary.com",
    "cambridge.org",
    "merriam-webster.com",
    "oxfordlearnersdictionaries.com",

    # Q&A
    "quora.com",
    "reddit.com",
    "zhihu.com",

    # Video
    "youtube.com",

    # Directories / Listings
    "turantcall.com",
    "collegenp.com",
    "yellowpagesnepal.com",
    "nepalyp.com",

    # Misc
    "scribd.com",
    "alison.com",
    "roblox.com",
}

# Social media that are allowed if no website exists
SOCIAL_DOMAINS = {
    "facebook.com",
}

# City / country keywords checked against page text
CITY_KEYWORDS = {
    "nepal",
    "kathmandu",
    "lalitpur",
    "bhaktapur",
    "pokhara",
    "biratnagar",
    "dharan",
    "hetauda",
    "janakpur",
    "butwal",
    "chitwan",
}


def get_domain(url: str) -> str:
    """
    Return the domain only.
    """

    try:
        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:
        return ""


def is_bad_domain(url: str) -> bool:
    """
    Returns True if the website should be ignored.
    """

    domain = get_domain(url)

    for bad in BAD_DOMAINS:
        if bad in domain:
            return True

    return False


def is_social(url: str) -> bool:
    """
    Check whether URL is a supported social page.
    """

    domain = get_domain(url)

    return any(site in domain for site in SOCIAL_DOMAINS)


def looks_nepal_based(url: str, text: str = "") -> bool:
    """
    Returns True if the URL/page appears Nepal related.

    Checks the domain suffix first (.np / .com.np), since that is
    an exact and reliable signal. Falls back to scanning the page
    text and URL for Nepali city or country names.
    """

    domain = get_domain(url)

    if domain.endswith(".np") or ".com.np" in domain:
        return True

    combined = (url + " " + text).lower()

    return any(keyword in combined for keyword in CITY_KEYWORDS)
