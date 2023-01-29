# Autoscout24.it Telegram Bot
Telegram bot for autoscout24.it written in Python which scrapes (for research purposes) all the new listings from a specific search and sends them to a Telegram chat or channel.

## Example message
![Example message on Telegram](example.png "Example message")

## How to use
- Install requirements
- Create a .env file in the project root and add the variables:
    - URL = go on [autoscout24.it](https://autoscout24.it), make the search you are interested in, copy here the URL from the browser
    - API_TOKEN = your Telegram API token for the bot
    - CHAT_ID = the ID of the chat/channel you want to send the messages to. To find the id, simply send a message in the chat/channel and forward it to https://t.me/JsonDumpBot. In the response you will find the chat ID
    - DB_URL = database url (default is "sqlite:///auto_scout24.db")
    - WAIT_BEFORE_NEXT = seconds to wait before the next search (default is 120)
    - WAIT_BEFORE_NEXT_PAGE = seconds to wait before the next page search (default is 10)
    - EXECUTE_ONCE = stop the bot after the first execution (default is False)
- Run the main.py