from requests import request
from bs4 import BeautifulSoup


def scrape(url, last_id):
    """
    Scrape the given url and extract all the listings

    :param url: Url to scrape
    :param last_id: ID of the last listing from the previously scraped results
    :return: Array of car listings
    """
    res = request('get', url, headers={
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'})
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        listings = soup.find_all("article")
        to_return = []
        found_previous_id = False
        for listing in listings:
            all_paragraphs = listing.find_all('p')
            all_spans = listing.find_all('span')
            if listing.get('id') != last_id:
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
                #auto['image'] = "".join(listing.find('img').get('src').rsplit("/")[:-1]) if listing.find('img') and len(next(listing.find('div').children).contents) > 0 else "-"
                to_return.append(auto)
            else:
                found_previous_id = True
                break
        return found_previous_id, to_return
    else:
        print(res.status_code)
        return []
