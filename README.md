# Google-Business-Reviews-Script
A collection of Python scripts that use the Google Places API to collect detailed business information — including ratings, reviews, phone numbers, websites, and locations — and export the results to Excel. Built for high efficiency using asyncio and aiohttp, the scripts make concurrent API calls while staying within Google’s rate limits.

⚙️ Key Features

Fully asynchronous architecture for faster API requests

Fetches and enriches business data with detailed profiles and reviews

Supports easy customization for any query (e.g., “HVAC,” “seafood restaurant,” “coffee shop”)

Exports clean, formatted Excel files

Includes error handling, deduplication, and structured outputs

🧩 Configuration

Replace GOOGLE_API_KEY with your valid Google Maps API key.

Update the CITIES list to specify target cities.

Adjust the QUERY variable to define the type of business you want to search.

💾 Output

Each run generates an Excel file containing:

Business Name

Address

Rating & Total Ratings

Phone Number

Website & Google Maps URL

Up to three recent reviews

🛠 Tech Stack

Language: Python 3

Libraries: asyncio, aiohttp, xlsxwriter, urllib.parse

APIs: Google Places Text Search & Details APIs
