import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import os
import re

URL = "https://chess-results.com/fed.aspx?lan=1&fed=BAR"
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

text = soup.get_text()

match = re.search(r"Last update\s*:\s*(.*)", text)

if not match:
    print("No update field found")
    exit()

update_str = match.group(1).strip()

update_time = datetime.strptime(update_str, "%d.%m.%Y %H:%M")
update_time = update_time.replace(tzinfo=timezone.utc)

now = datetime.now(timezone.utc)

diff = (now - update_time).total_seconds()

# Notify if updated within last 2 minutes
if 0 <= diff <= 120:
    requests.post(WEBHOOK, json={
        "content": f"♟ Chess Results BAR updated at {update_str}"
    })
