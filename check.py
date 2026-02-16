import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://chess-results.com/fed.aspx?lan=1&fed=BAR"
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

times = []

# Find all cells containing update times
cells = soup.find_all("td", class_="CRnowrap")

for cell in cells:
    text = cell.get_text(" ", strip=True)

    # Example matches:
    # 3 Hours 13 Min.
    # 2 Days 7 Hours
    # 19 Hours 26 Min.
    # 36 Days 10 Hours
    
    days = re.search(r"(\d+)\s*Days?", text)
    hours = re.search(r"(\d+)\s*Hours?", text)
    mins = re.search(r"(\d+)\s*Min", text)

    total_minutes = 0

    if days:
        total_minutes += int(days.group(1)) * 1440
    if hours:
        total_minutes += int(hours.group(1)) * 60
    if mins:
        total_minutes += int(mins.group(1))

    if total_minutes > 0:
        times.append(total_minutes)

if not times:
    print("No time values found")
    exit()

latest_update = min(times)

print("Newest update (minutes ago):", latest_update)

# Notify if update happened within 2 minutes
if latest_update <= 2:
    requests.post(WEBHOOK, json={
        "content": f"♟ Barbados chess results updated {latest_update} minute(s) ago!"
    })
