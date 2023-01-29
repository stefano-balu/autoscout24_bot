import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('telegram')


class TelegramBot:
    def __init__(self, api_token, chat_id):
        self.bot = Bot(token=api_token, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot)
        self.chat_id = chat_id

    async def send_message(self, user_id: int, text: str, disable_notification: bool = False) -> bool:
        """
        Safe messages sender

        :param user_id:
        :param text:
        :param disable_notification:
        :return:
        """
        try:
            await self.bot.send_message(user_id, text, disable_notification=disable_notification)
        except exceptions.BotBlocked:
            log.error(f"Target [ID:{user_id}]: blocked by user")
        except exceptions.ChatNotFound:
            log.error(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            return await send_message(user_id, text)  # Recursive call
        except exceptions.UserDeactivated:
            log.error(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            log.exception(f"Target [ID:{user_id}]: failed")
        else:
            log.info(f"Target [ID:{user_id}]: success")
            return True
        return False

    async def broadcaster(self, message) -> int:
        """
        Simple broadcaster

        :param message: Message to be sent
        :return: True if message was sent, False otherwise
        """
        try:
            await self.send_message(str(self.chat_id), message)
        finally:
            log.info("Message successfully sent.")

    def get_dispatcher(self):
        """
        Get the dispatcher

        :return: Value of the dispatcher
        """
        return self.dp
