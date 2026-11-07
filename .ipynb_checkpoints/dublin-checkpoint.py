import json
from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime

DATE = datetime.today().strftime("%d-%m-%Y")
print(DATE)

def get_dublin(page):
    try:
        response = requests.get("https://www.daft.ie/sharing/dublin", params={"page": page}, impersonate="chrome")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            data = soup.find('script', id='__NEXT_DATA__')
            return json.loads(data.text), response.status_code

        return None, response.status_code

    except Exception as e:
        print(f"Network/Request error on page {page}: {e}")
        return None, 0


page = 1
while True:
    print("Page", page)
    data, status = get_dublin(page)

    if status != 200:
        print(status)
        break

    if not data:
        print("No data found, stopping")
        break


    with open(f"data/daft_{DATE}.json", 'w') as f:
        json.dump(data, f)
        

    page += 1
