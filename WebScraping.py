# import required libraries
import os
import re
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
# This helps you keep API keys private instead of hardcoding them
load_dotenv()
API_KEY = os.getenv("API_KEY")

# If no API key is found, raise an error
if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in your .env file")

# Regions and categories to fetch data for and Each region has a list of business categories
regions = {
    "United States - Kansas": [
        "Clothing & Apparel", "Electronics & Gadgets", "Beauty & Personal Care", "Jewelry & Accessories",
        "Furniture & Décor", "Legal Services", "Accounting & Tax", "Consulting", "Real Estate Agency",
        "Financial Planning", "Hospitals & Clinics", "Fitness Centers", "Restaurants", "Cafes",
        "Catering Services", "Coaching Institutes"
    ],
    "Canada - Nunavut": [
        "Real Estate Agency", "Financial Planning", "Hospitals & Clinics", "Fitness Centers",
        "Restaurants", "Cafes", "Catering Services", "Coaching Institutes", "Clothing & Apparel",
        "Electronics & Gadgets", "Beauty & Personal Care", "Jewelry & Accessories", "Furniture & Decor",
        "Legal Services", "Accounting & Tax", "Consulting"
    ]
}

# Fetches businesses for a given region & category using Google Places API
def get_places(region, category, limit=10):
    # API endpoint: Text Search
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{category} in {region}",  
        "key": API_KEY
    }

    results = []       # Store final businesses
    seen_emails = set()  # Track unique emails (avoid duplicates)

    # Loop until we reach the limit or run out of results
    while len(results) < limit and url:
        response = requests.get(url, params=params)
        data = response.json()

        # Loop over businesses returned by the API
        for place in data.get("results", []):
            place_id = place["place_id"]

            # API endpoint: Place Details (fetch phone, website, address, etc.)
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place_id,
                "fields": "name,formatted_phone_number,formatted_address,website",
                "key": API_KEY
            }
            details = requests.get(details_url, params=details_params).json().get("result", {})

            # Extract details
            business_name = details.get("name")
            phone = details.get("formatted_phone_number", "")
            address = details.get("formatted_address", "")
            website = details.get("website", "")

            # Try to scrape email from the website HTML (if available)
            email = ""
            if website:
                try:
                    site_html = requests.get(website, timeout=5).text
                    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", site_html)
                    if match:
                        email = match.group(0)
                except:
                    pass  # If website not accessible, ignore

            # Add business only if it has a name + unique email
            if business_name and email and email not in seen_emails:
                results.append({
                    "Business Name": business_name,
                    "Email": email,
                    "Phone": phone,
                    "Website": website,
                    "Address": address,
                    "Category": category
                })
                seen_emails.add(email)

            # Stop if we reached the limit
            if len(results) >= limit:
                break

        # Handle pagination: Google returns next_page_token if more results are available
        url = None
        if "next_page_token" in data:
            time.sleep(2)  # Small delay required by API before next_page_token works
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                "pagetoken": data["next_page_token"],
                "key": API_KEY
            }

    return results

# Collect data for all regions and categories
all_data = {}
for region, categories in regions.items():
    region_data = []
    for category in categories:
        print(f"Fetching: {region} - {category}")
        businesses = get_places(region, category, limit=10)
        region_data.extend(businesses)

        # Validation: If fewer than 10 businesses found, add a note
        if len(businesses) < 10:
            region_data.append({
                "Business Name": "Less than 10 records available for this category",
                "Email": "",
                "Phone": "",
                "Website": "",
                "Address": "",
                "Category": ""
            })

    # Store all category data for this region
    all_data[region] = region_data

# Save collected data into an Excel file
# Each region gets its own sheet
writer = pd.ExcelWriter("Kansas_Business.xlsx", engine="openpyxl")
for region, records in all_data.items():
    df = pd.DataFrame(records)
    # Excel sheet names are limited to 31 chars, so truncate
    df.to_excel(writer, sheet_name=region[:31], index=False)
writer.close()

print("Data saved to Kansas_Business.xlsx")
