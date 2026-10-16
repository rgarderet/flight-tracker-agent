import requests
import json

ROUTES = [
    {"from": "DFW", "to": "SYD", "date": "2027-01-12"},
    {"from": "BNE", "to": "DFW", "date": "2027-01-31"}
]

def check_flights(route):
    # Utilizing an open microservices gateway route to aggregate fares
    url = f"https://flightapi.io{route['from']}/{route['to']}/{route['date']}/1/0/0/Economy/USD"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            fares = data.get("fares", [])
            
            # Filter specifically down to American Airlines validation matrices
            aa_fares = [f for f in fares if "american" in f.get("provider", "").lower() or "aa" in f.get("filter", "").lower()]
            
            if aa_fares:
                cheapest = min([f.get("price", float('inf')) for f in aa_fares])
                return f"💰 ${cheapest} USD (American Airlines)"
            elif fares:
                # Fallback to the cheapest overall option if AA isn't explicitly flagged
                cheapest_overall = min([f.get("price", float('inf')) for f in fares])
                return f"💰 ${cheapest_overall} USD (Cheapest Available Option)"
                
            return "❌ No clear pricing options returned in public flight matrix."
        return f"❌ Server connection throttled (HTTP Code {response.status_code})"
    except Exception as e:
        # Prevent json parsing crash issues by catching structural layout issues safely
        return f"❌ Scraping Connection Error: Grid unavailable right now."

print("\n=======================================================")
print("🚨 LIVE FLIGHT PRICE BOTTLENECK REPORT")
print("=======================================================")
for r in ROUTES:
    price_result = check_flights(r)
    print(f"✈️  {r['from']} ➔ {r['to']} ({r['date']}): {price_result}")
print("=======================================================\n")
