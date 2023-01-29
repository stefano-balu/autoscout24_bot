import json
import time
from dataclasses import dataclass
from os import getenv
from typing import List

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


@dataclass
class Config:
    API_TOKEN: str
    CHAT_ID: str
    URLS: List[str] = list
    MAX_PAGES: int = 1
    WAIT_BEFORE_NEXT: int = 60*60*6  # 6 hours
    WAIT_BEFORE_NEXT_PAGE: int = 10  # 6 hours
    DB_URL: str = "sqlite:///auto_scout24.db"

    @classmethod
    def load(cls):
        with open("config.json", "r") as f:
            conf = json.load(f)

        conf = {key: getenv(key, conf.get(key)) for key in cls.__annotations__.keys() if getenv(key, conf.get(key))}

        # Merge URL parameter into URLS
        conf.setdefault("URLS", [])
        url = conf.pop("URL", None)

        if url:
            conf["URLS"].insert(0, url)

        return cls(**cls.parse_types(conf))

    @staticmethod
    def parse_types(conf: dict):
        return {
            k: _mapper(conf[k])
            for k, _mapper in [
                ("API_TOKEN", str),
                ("CHAT_ID", str),
                ("DB_URL", str),
                ("URLS", lambda x: x),
                ("MAX_PAGES", int),
                ("WAIT_BEFORE_NEXT", int),
                ("WAIT_BEFORE_NEXT_PAGE", int),
            ]
            if k in conf
        }


def start(urls, db):
    """
    Control the scraping process

    :param urls: Listo of url to scrape
    :param db: database session
    :return: ID of the last scraped listing
    """
    stop = False
    n_page = 0

    for n, url in enumerate(urls, start=1):
        while not stop:
            n_page += 1
            stop, results = scraper.scrape(f"{url}&page={n_page}", db)

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
                    f"Ricerca numero: {n}\n",
                    f"\n<a href='{res['url']}'>Link</a>"
                ]
                logger.info("Found new car: %s", res)
                message = ''.join(message)
                dp = bot.get_dispatcher()
                executor.start(dp, bot.broadcaster(message))
                time.sleep(1)

            if n_page == config.MAX_PAGES:
                stop = True

            if not stop:
                time.sleep(config.WAIT_BEFORE_NEXT_PAGE)

        logger.info(f"scraped {n_page} pages")


if __name__ == '__main__':
    config = Config.load()

    bot = telegram.TelegramBot(config.API_TOKEN, config.CHAT_ID)
    engine = create_engine(config.DB_URL)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    while True:
        session.begin()
        start(config.URLS, session)
        session.close()
        time.sleep(config.WAIT_BEFORE_NEXT)
