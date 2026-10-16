import os
import requests

# Fetch secrets from GitHub
SERPAPI_KEY = os.environ.get('SERPAPI_KEY')

# Your exact bottleneck flights
ROUTES = [
    {"from": "DFW", "to": "SYD", "date": "2027-01-12"},
    {"from": "BNE", "to": "DFW", "date": "2027-01-31"}
]

def check_flights(route):
    url = "https://serpapi.com"
    params = {
        "engine": "google_flights",
        "departure_id": route["from"],
        "arrival_id": route["to"],
        "outbound_date": route["date"],
        "currency": "USD",
        "hl": "en",
        "gl": "us",
        "api_key": SERPAPI_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_flights = data.get("best_flights", []) + data.get("other_flights", [])
            aa_flights = [f for f in all_flights if "american" in f.get("airline", "").lower()]
            
            if aa_flights:
                cheapest = min(aa_flights, key=lambda x: x.get("price", float('inf')))
                return f"💰 ${cheapest.get('price')} USD (American Airlines)"
            return "❌ No American Airlines flights found for this date matrix."
        return f"❌ API Error (Status Code: {response.status_code})"
    except Exception as e:
        return f"❌ Network Request Error: {str(e)}"

# Generate clear visual markers directly into the GitHub Runner interface console logs
print("\n=======================================================")
print("🚨 LIVE FLIGHT PRICE BOTTLENECK REPORT")
print("=======================================================")
for r in ROUTES:
    price_result = check_flights(r)
    print(f"✈️  {r['from']} ➔ {r['to']} ({r['date']}): {price_result}")
print("=======================================================\n")

