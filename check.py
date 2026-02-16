import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import os

URL = "https://chess-results.com/fed.aspx?lan=1&fed=BAR"
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

text = soup.get_text()

# find Last update text
import re
match = re.search(r"Last update\s*:\s*(.*)", text)

if not match:
    print("No update field found")
    exit()

update_str = match.group(1).strip()

# Example format: 16.02.2026 14:32
update_time = datetime.strptime(update_str, "%d.%m.%Y %H:%M")
update_time = update_time.replace(tzinfo=timezone.utc)

now = datetime.now(timezone.utc)

diff = (now - update_time).total_seconds()

if diff <= 60:
    requests.post(WEBHOOK, json={
        "content": f"Chess Results BAR updated at {update_str}"
    })
