import requests

# Target bottlenecks definitions
ROUTES = [
    {"from": "DFW", "to": "SYD", "date": "12/01/2027"},  # Format: DD/MM/YYYY for the open engine
    {"from": "BNE", "to": "DFW", "date": "31/01/2027"}
]

def check_flights(route):
    # Completely open, key-free public flight routing database
    url = "https://skypicker.com"
    params = {
        "fly_from": route["from"],
        "fly_to": route["to"],
        "date_from": route["date"],
        "date_to": route["date"],
        "select_airlines": "AA",  # Limits queries specifically to American Airlines
        "curr": "USD",
        "partner": "picky",       # Default free public access token
        "v": 3
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            flight_data = data.get("data", [])
            
            if flight_data:
                # Find the absolute cheapest option returned in the database matrix
                cheapest_price = min([f.get("price", float('inf')) for f in flight_data])
                return f"💰 ${cheapest_price} USD (American Airlines)"
            return "❌ No American Airlines flights found in database matrix for this date."
        return f"❌ Server Response Error (Code: {response.status_code})"
    except Exception as e:
        return f"❌ Network Connection Error: {str(e)}"

print("\n=======================================================")
print("🚨 LIVE FLIGHT PRICE BOTTLENECK REPORT (KEYLESS)")
print("=======================================================")
for r in ROUTES:
    price_result = check_flights(r)
    # Convert display date format back to normal readability
    display_date = "-".join(reversed(r["date"].split("/")))
    print(f"✈️  {r['from']} ➔ {r['to']} ({display_date}): {price_result}")
print("=======================================================\n")

