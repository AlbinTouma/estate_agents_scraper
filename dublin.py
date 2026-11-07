import json
from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from dataclasses import dataclass

@dataclass
class State:
    page: int
    totalPages: int
    totalResults: int
    displayingTo: int

    def to_dict(self):
        return {"page": self.page, "total_pages": self.totalPages, "total_listings": self.totalResults, "collected": self.displayingTo}

scraper = State(0,0,0,0)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)-15s %(levelname)-8s %(message)s')
DATE = datetime.today().strftime("%d-%m-%Y")


def get_dublin(page):
    response = None
    try:
        response = requests.get("https://www.daft.ie/sharing/dublin", params={"page": page}, impersonate="chrome", timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:  
        logging.error(f'HTTP Error occured: {e}')
        return response

def parse_dublin(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('script', id='__NEXT_DATA__')
    return json.loads(data.text)


def update_state(data):
    scraper.page =   data.get('props').get('pageProps').get('paging').get('currentPage')
    scraper.totalPages = data.get('props').get('pageProps').get('paging').get('totalPages')
    scraper.totalResults = data.get('props').get('pageProps').get('paging').get('totalResults')
    scraper.displayingTo = data.get('props').get('pageProps').get('paging').get('displayingTo')




page = 1    
while True: 
    response = get_dublin(page)
    page += 1

    if response.status_code != 200:
        print(f"End  page {page} due to {response.status_code}")
        break

    if not response:
        print("No data found, stopping")
        break

    data = parse_dublin(response)
    update_state(data)
    print(scraper.to_dict())


    with open(f"data/daft_{DATE}.jsonl", 'a') as f:
        f.write(json.dumps(data) + "\n")
        


logging.info(scraper.to_dict())
