import time
from os import getenv

from aiogram.utils import executor
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from scraper import scraper
from telegram_module import telegram
from utils import get_logger

load_dotenv()

logger = get_logger()


def start(url, db):
    """
    Control the scraping process

    :param url: Url to scrape
    :param db: database session
    :return: ID of the last scraped listing
    """
    n_page = 0

    while True:
        n_page += 1
        stop, results = scraper.scrape(f"{url}&page={n_page}", db)

        if stop:
            break

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
            logger.info("Found new car: %s", res)
            message = ''.join(message)
            dp = bot.get_dispatcher()
            executor.start(dp, bot.broadcaster(message))
            time.sleep(1)

        time.sleep(int(getenv("WAIT_BEFORE_NEXT_PAGE", 10)))

    logger.info(f"scraped {n_page} pages")


if __name__ == '__main__':
    if not(getenv("API_TOKEN") and getenv('CHAT_ID') and getenv("URL")):
        raise Exception('One or more environment variables are missing!')

    bot = telegram.TelegramBot(getenv("API_TOKEN"), getenv('CHAT_ID'))
    engine = create_engine(getenv("DB_URL", "sqlite:///auto_scout24.db"))
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    while True:
        session.begin()
        start(getenv("URL"), session)
        session.close()

        if getenv("EXECUTE_ONCE", "false").lower() == "true":
            break

        time.sleep(int(getenv("WAIT_BEFORE_NEXT", 120)))
