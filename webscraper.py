import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import time

# Your Telegram bot token
bot_token = '7361437885:AAEbYONVyllYcAAjdR2P_e9ZM3TgBJk3QHs'
# Your chat ID (you can get this from the BotFather or by getting updates from the bot)
chat_id = '-1002149330170'

# Initialize the bot
bot = Bot(token=bot_token)

def fetch_live_score():
    url = 'https://www.espncricinfo.com/series/west-indies-in-england-2024-1385669/england-vs-west-indies-1st-test-1385691/live-cricket-score'
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Failed to retrieve webpage. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    live_score_element = soup.find('div', class_='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1')

    if live_score_element:
        live_score = live_score_element.get_text(strip=True)
        return live_score
    else:
        return "Live score element not found."

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print("Message sent successfully!")
    except TelegramError as e:
        print(f"Failed to send message. Error: {e}")

async def main():
    while True:
        # Fetch the live score
        live_score = fetch_live_score()
        print(f"Live Match: {live_score}")

        # Send the live score to Telegram
        await send_telegram_message(live_score)

        # Wait for a specified interval (e.g., 60 seconds) before fetching the scores again
        await asyncio.sleep(60)  # Adjust the interval as needed

# Run the main function in the asyncio event loop
if _name_ == "_main_":
    asyncio.run(main())