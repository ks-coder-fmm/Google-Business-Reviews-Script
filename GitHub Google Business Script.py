import asyncio
import aiohttp
import xlsxwriter

# --- CONFIGURATION ---
GOOGLE_API_KEY = [YOUR API KEY]  # Replace with your actual key
PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
CITIES = ["Your City, Your State"] #Replace with the city and state you are looking for
QUERY = "Veterinarian"

# --- GLOBALS ---
results = []
place_ids_seen = set()
semaphore = asyncio.Semaphore(5)

# --- ASYNC FUNCTIONS ---
async def fetch_place_details(session, place_id):
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,reviews,formatted_address,website,url,formatted_phone_number",
        "key": GOOGLE_API_KEY
    }
    try:
        async with semaphore:
            async with session.get(PLACE_DETAILS_URL, params=params, timeout=15) as resp:
                data = await resp.json()
                return data.get("result", {})
    except Exception as e:
        print(f"⚠️ Error fetching details for place_id {place_id}: {e}")
        return {}

async def search_businesses(session, city):
    params = {
        "query": f"{QUERY} in {city}",
        "key": GOOGLE_API_KEY
    }
    try:
        async with semaphore:
            async with session.get(PLACES_TEXT_SEARCH_URL, params=params, timeout=15) as resp:
                data = await resp.json()
                places = data.get("results", [])
                tasks = []
                for place in places:
                    place_id = place.get("place_id")
                    if place_id and place_id not in place_ids_seen:
                        place_ids_seen.add(place_id)
                        tasks.append(fetch_place_details(session, place_id))
                return await asyncio.gather(*tasks)
    except Exception as e:
        print(f"⚠️ Error searching for businesses in {city}: {e}")
        return []

# --- MAIN ASYNC RUNNER ---
async def run_scraper():
    async with aiohttp.ClientSession() as session:
        tasks = [search_businesses(session, city) for city in CITIES]
        all_results = await asyncio.gather(*tasks)
        for city_results in all_results:
            for business in city_results:
                results.append({
                    "name": business.get("name", ""),
                    "address": business.get("formatted_address", ""),
                    "rating": business.get("rating", ""),
                    "total_ratings": business.get("user_ratings_total", ""),
                    "website": business.get("website", ""),
                    "map_url": business.get("url", ""),
                    "phone": business.get("formatted_phone_number", ""),
                    "reviews": " | ".join([rev.get("text", "") for rev in business.get("reviews", [])[:3]])
                })

# --- EXCEL WRITER ---
def write_to_excel():
    workbook = xlsxwriter.Workbook("google_business_veterinarians.xlsx")
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({'bold': True, 'bg_color': '#CFE2F3'})
    headers = ["Business Name", "Address", "Rating", "# of Ratings", "Phone", "Website", "Map URL", "Sample Reviews"]

    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    for row_num, business in enumerate(results, start=1):
        worksheet.write(row_num, 0, business["name"])
        worksheet.write(row_num, 1, business["address"])
        worksheet.write(row_num, 2, business["rating"])
        worksheet.write(row_num, 3, business["total_ratings"])
        worksheet.write(row_num, 4, business["phone"])
        worksheet.write(row_num, 5, business["website"])
        worksheet.write(row_num, 6, business["map_url"])
        worksheet.write(row_num, 7, business["reviews"])

    workbook.close()
    print(f"✅ Done! {len(results)} plumbers saved to Excel.")

# --- MAIN ---
def main():
    asyncio.run(run_scraper())
    write_to_excel()

if __name__ == "__main__":
    main()
