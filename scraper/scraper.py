from bs4 import BeautifulSoup
from requests import request

from database.models import AutoScout24
from utils import get_logger

logger = get_logger()

REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'}


def scrape(url, db):
    """
    Scrape the given url and extract all the listings

    :param db: database session
    :param url: Url to scrape
    :return: Array of car listings
    """
    logger.info("Search url: %s", url)
    res = request('get', url, headers=REQUEST_HEADERS)

    if not res.ok:
        logger.error("Invalid response status: %d", res.status_code)
        return False, []

    soup = BeautifulSoup(res.text, 'lxml')
    listings = soup.find_all("article")

    results = []
    for listing in listings:
        all_paragraphs = listing.find_all('p')
        all_spans = listing.find_all('span')
        auto = {
            'id': listing.get('id'),
            'title': listing.find('h2').contents[0] + " " + (listing.find('h2').next_sibling.string if listing.find('h2').next_sibling.string else ""),
            'price_euro': all_paragraphs[0].string.split("€")[1].split(",")[0].lstrip(),
            'classification': all_paragraphs[1].string,
            'kilometers': all_spans[1].string,
            'year': all_spans[2].string,
            'horsepower': all_spans[3].string,
            'condition': all_spans[4].string,
            'owners': all_spans[5].string,
            'shift': all_spans[6].string,
            'fuel': all_spans[7].string,
            'fuel_consumption': all_spans[8].string,
            'co2': all_spans[9].string,
            'seller_type': all_spans[10].contents[0],
            'seller_location': all_spans[-1].string if all_spans[-1].string else "-",
            'url': "https://www.autoscout24.it" + listing.find('a').get('href')
        }

        auto_id = auto['id']
        if auto_id:
            obj = db.query(AutoScout24).get(auto_id)
            if not obj:
                obj = AutoScout24(**auto)
                db.add(obj)
                db.commit()
                results.append(auto)
    return not listings, results
