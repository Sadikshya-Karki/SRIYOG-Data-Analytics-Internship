"""
extractor.py

Extract information from training provider websites.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from filters import looks_nepal_based

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PHONE_PATTERN = re.compile(r"(\+977[- ]?)?(98\d{8}|97\d{8}|96\d{8}|01[- ]?\d{7})")
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

LOCATIONS = [
    "Kathmandu","Lalitpur","Bhaktapur","Pokhara","Biratnagar",
    "Butwal","Dharan","Janakpur","Hetauda","Nepalgunj","Chitwan"
]

CONTACT_HINTS = ("contact","contact-us","contactus","about","reach")

def _get(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r

def _clean_title(title:str)->str:
    for sep in ["|","-","–","—"]:
        if sep in title:
            title = title.split(sep)[0]
    return " ".join(title.split()).strip()

def scrape_site(url:str)->dict:
    data = {
        "Training Providers":"",
        "Location":"",
        "Contact":"",
        "Links":url,
        "Is Nepal":False,
    }
    try:
        resp = _get(url)
    except Exception:
        return data

    soup = BeautifulSoup(resp.text,"html.parser")

    if soup.title:
        data["Training Providers"] = _clean_title(soup.title.get_text(" ",strip=True))

    text = soup.get_text(" ", strip=True)

    # Try contact/about page
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if any(h in href for h in CONTACT_HINTS):
            try:
                page = _get(urljoin(url,a["href"]))
                text += " " + BeautifulSoup(page.text,"html.parser").get_text(" ",strip=True)
            except Exception:
                pass
            break

    phone = PHONE_PATTERN.search(text)
    if phone:
        data["Contact"] = phone.group().strip()

    email = EMAIL_PATTERN.search(text)
    if email:
        data["Email"] = email.group().strip()

    lower = text.lower()
    for city in LOCATIONS:
        if city.lower() in lower:
            data["Location"] = city
            break

    # A matched Nepali phone number is itself a strong Nepal signal,
    # on top of the domain/text based check.
    data["Is Nepal"] = bool(phone) or looks_nepal_based(url, text)

    return data

if __name__ == "__main__":
    import sys
    test = sys.argv[1] if len(sys.argv)>1 else "https://skillnepal.com.np"
    from pprint import pprint
    pprint(scrape_site(test))
