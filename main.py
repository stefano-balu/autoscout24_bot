from dotenv import load_dotenv
load_dotenv()
from os import getenv
from telegram_module import telegram
from aiogram.utils import executor
from scraper import scraper
import time


def start(url, last_id, bot):
    """
    Control the scraping process

    :param url: Url to scrape
    :param last_id: ID of the last listing from the previously scraped results
    :param bot: Instance of the Telegram bot
    :return: ID of the last scraped listing
    """
    n_page = 0
    found_previous_id = False

    while(not found_previous_id):
        n_page += 1
        # Build the url with the page number
        found_previous_id, results = scraper.scrape(
            f"{url}&page={n_page}", last_id)

        # Build and send the messages via telegram
        for res in results:
            message = [
                f"<b>{res['title']}</b>\n",
                f"Anno: {res['year']}\n",
                f"Chilometraggio: {res['kilometers']}\n",
                f"Potenza: {res['horsepower']}\n",
                f"Cambio: {res['shift']}\n",
                f"Carburante: {res['fuel']}\n",
                f"Consumo: {res['fuel_consumption']}\n",
                f"Condizione: {res['condition']}\n",
                f"Proprietari: {res['owners']}\n",
                f"Inquinamento: {res['co2']}\n",
                f"Venditore: {res['seller_type']}\n",
                f"Località: {res['seller_location']}\n",
                f"<b>PREZZO</b>: €{res['price_euro']}\n",
                f"\n<a href='{res['url']}'>Link</a>"
            ]
            message = ''.join(message)
            dp = bot.get_dispatcher()
            executor.start(
                dp,
                bot.broadcaster(message)
            )
            time.sleep(3)

        # Save the previous last id and update the last id
        previous_last_id = last_id
        if len(results) != 0:
            last_id = results[0]['id']

        # If the previous last was empty, it means it's the first request
        # By design, the first request only scrapes the first page
        if previous_last_id == "":
            break
    print(f"scraped {n_page} pages")
    return last_id


# Initialize and start the scraping
if(not(getenv("API_TOKEN") and getenv('CHAT_ID') and getenv("URL"))):
    print('One or more environment variables are missing!')
else:
    last_id = ""
    bot = telegram.Telegram_Bot(getenv("API_TOKEN"), getenv('CHAT_ID'))
    
    while(True):
        last_id = start(getenv("URL"), last_id, bot)
        time.sleep(int(getenv("WAIT_BEFORE_NEXT", 120)))
