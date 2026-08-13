"""
scraper.py

Search all HomeSewa services, scrape provider details,
deduplicate providers, keep Nepal-based providers only,
and export to Excel.
"""

import time
import pandas as pd
from search import search_service
from extractor import scrape_site

SERVICES = {
    "Salon at Home":"salon beauty parlour training",
    "Bridal Makeup":"bridal makeup training",
    "Chef at Home":"chef cooking training",
    "Massage Therapy":"massage therapy training",
    "Spa at Home":"spa training",
    "Physiotherapy":"physiotherapy training",
    "Handyman":"handyman training",
    "Carpentry":"carpentry training",
    "Plumbing":"plumbing training",
    "Electrical Repairs":"electrical repair training",
    "Tiling":"tiling training",
    "Washing Machine Repair":"washing machine repair training",
    "Home Automation":"home automation training",
    "EV Charger Installation":"EV charger installation training",
    "AC Services":"AC repair technician training",
    "Painting":"house painter training",
    "Indoor Planting":"indoor plant nursery training",
    "CCTV Services":"CCTV camera installation training",
    "Drywall Repair":"gypsum board drywall training",
    "Modular Kitchen":"modular kitchen training",
    "Parqueting":"parquet flooring training",
    "Home Renovation":"home renovation contractor training",
    "RO Water Purifying":"RO water purifier repair training",
    "Garden Care":"gardening landscaping training",
    "Pest Control":"pest control training",
    "Masonry Repair":"masonry training",
    "Deep Cleaning":"housekeeping deep cleaning training",
    "Packing and Moving":"packers movers training",
    "Airbnb Maintenance":"home maintenance handyman training",
    "Refrigerator Repair":"refrigerator repair training",
}

OUTPUT_FILE = "training_providers.xlsx"

COLUMN_ORDER = [
    "#",
    "HomeSewa Service",
    "Training Providers",
    "Location",
    "Contact",
    "Links",
]

def save(rows):
    df = pd.DataFrame(rows)
    if not df.empty:
        df.insert(0, "S.N.", range(1, len(df)+1))
        df = df[COLUMN_ORDER]
    df.to_excel(OUTPUT_FILE, index=False)

def main():
    rows=[]
    visited_urls=set()

    total=len(SERVICES)
    start_time = time.time()

    for i,(service,keyword) in enumerate(SERVICES.items(),1):
        elapsed = time.time() - start_time
        print(f"\n{'='*70}")
        print(f"[{i}/{total}] {service}  (elapsed {elapsed:.0f}s)")
        print("="*70)

        results=search_service(keyword)

        print(f"Found {len(results)} candidate websites")

        kept = 0
        skipped_not_nepal = 0

        for r in results:
            url=r["url"]

            if url in visited_urls:
                continue

            visited_urls.add(url)

            print("Scraping:",url)

            info=scrape_site(url)

            if not info.get("Is Nepal"):
                skipped_not_nepal += 1
                continue

            rows.append({
                "HomeSewa Service":service,
                "Training Providers":info.get("Training Providers") or r.get("title",""),
                "Location":info.get("Location",""),
                "Contact":info.get("Contact",""),
                "Links":url,
            })

            kept += 1
            save(rows)
            time.sleep(1)

        print(f"Kept {kept} Nepal-based providers, skipped {skipped_not_nepal} non-Nepal")

    print(f"\nFinished. Saved {len(rows)} providers to {OUTPUT_FILE}")

if __name__=="__main__":
    main()
