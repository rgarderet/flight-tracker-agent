import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fetch secrets from GitHub
SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
GMAIL_USER = os.environ.get('RECEIVER_EMAIL')      # remy.garderet@gmail.com
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')  # Your 16-character Google App Password

# Your exact bottleneck flights (Updated to target January 2027 based on your request)
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
            # Combine best and other flights matrix arrays
            all_flights = data.get("best_flights", []) + data.get("other_flights", [])
            
            # Filter specifically for American Airlines
            aa_flights = [f for f in all_flights if "american" in f.get("airline", "").lower()]
            
            if aa_flights:
                cheapest = min(aa_flights, key=lambda x: x.get("price", float('inf')))
                return f"💰 ${cheapest.get('price')} USD"
            return "❌ No American Airlines flights found."
        return "❌ API Error"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Generate Email Content
email_body = "<h3>✈️ Daily Flight Tracker Bottlenecks</h3><hr>"
for r in ROUTES:
    price_result = check_flights(r)
    email_body += f"<p><strong>{r['from']} → {r['to']}</strong> ({r['date']}): {price_result}</p>"

# Send Email via Gmail SMTP
msg = MIMEMultipart()
msg['From'] = GMAIL_USER
msg['To'] = GMAIL_USER
msg['Subject'] = '🚨 Daily Flight Price Update'
msg.attach(MIMEText(email_body, 'html'))

try:
    server = smtplib.SMTP('://gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
    server.quit()
    print("Success! Email sent.")
except Exception as e:
    print(f"Email failed: {e}")
