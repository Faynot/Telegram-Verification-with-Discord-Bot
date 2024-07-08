import telebot
import random
import string
import requests
import json
import time
from telebot import types
from threading import Thread

API_TOKEN = 'PASTE_TOKEN'
CHANNEL_ID = 'PASTE_ID'
DISCORD_BOT_URL = 'PASTE_YOURE_NGROK_URL/verify'
DISCORD_REMOVE_USER_URL = 'PASTE_YOURE_NGROK_URL/remove_user'

bot = telebot.TeleBot(API_TOKEN)


try:
    with open('linked_users.json', 'r') as f:
        linked_users = json.load(f)
except FileNotFoundError:
    linked_users = {}


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def save_linked_users():
    with open('linked_users.json', 'w') as f:
        json.dump(linked_users, f, indent=4)


def is_user_in_channel(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            print(f"User {user_id} do not channel member.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def send_verification_request_to_discord(user_id, discord_username, code):
    try:
        response = requests.post(DISCORD_BOT_URL, json={'telegram_id': user_id, 'discord_username': discord_username, 'code': code})
        if response.status_code == 200:
            print("HTTP request sent to discord bot.")
        else:
            print(f"Error sending HTTP request to Discord bot. Error code: {response.status_code}")
    except Exception as e:
        print(f"Error when making an HTTP request in a Discord bot: {e}")


def send_user_removal_notification_to_discord(user_id, discord_username):
    try:
        response = requests.post(DISCORD_REMOVE_USER_URL, json={'telegram_id': user_id, 'discord_username': discord_username})
        if response.status_code == 200:
            print("An HTTP request to delete a user was successfully sent to the Discord bot.")
        else:
            print(f"Error when sending an HTTP request to delete a user in a Discord bot. Error code: {response.status_code}")
    except Exception as e:
        print(f"Error when executing an HTTP request to delete a user in a Discord bot: {e}")


def check_and_send_verification(user_id, discord_username):
    if is_user_in_channel(user_id):
        code = generate_code()
        bot.send_message(user_id, f"🤓 Your verification code: {code}.\nSend it to the bot on Discord: YoureVerifyBot#0000.")

        linked_users[user_id] = {
            'discord_username': discord_username,
            'verification_code': code
        }
        save_linked_users()

        send_verification_request_to_discord(user_id, discord_username, code)
        bot.send_message(user_id, "✨Information has been sent to the bot in Discord.\nPlease enter your code in the bot's Discord.")
    else:
        bot.send_message(user_id, "😭 You are not in the channel. Unable to verify.")


def check_linked_users():
    while True:
        for user_id in list(linked_users.keys()):
            if not is_user_in_channel(user_id):
                discord_username = linked_users[user_id]['discord_username']
                send_verification_request_to_discord(user_id, discord_username, "")

                del linked_users[user_id]
                save_linked_users()
                print(f"User {user_id} has been removed from the list of linked users.")
                send_user_removal_notification_to_discord(user_id, discord_username)
        time.sleep(5)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🌵 Welcome to the Telegram and Discord verification bot! Type /link to link your Telegram with your Discord account.")

@bot.message_handler(commands=['link'])
def ask_discord_username(message):
    bot.send_message(message.chat.id, "🔧 Enter your Discord username:")

@bot.message_handler(func=lambda message: True)
def process_discord_username(message):
    user_id = message.from_user.id
    discord_username = message.text

    if is_user_in_channel(user_id):
        code = generate_code()
        bot.send_message(message.chat.id, f"🤓 Your verification code: {code}.\nSend it to the bot on Discord: YoureVerifyBot#0000.")

        linked_users[user_id] = {
            'discord_username': discord_username,
            'verification_code': code
        }
        save_linked_users()

        response = requests.post(DISCORD_BOT_URL, json={'telegram_id': user_id, 'discord_username': discord_username, 'code': code})
        if response.status_code == 200:
            bot.send_message(message.chat.id, "✨ Information has been sent to the bot in Discord.\nPlease enter your code in the bot's Discord.")
        else:
            bot.send_message(message.chat.id, f"Verification error. Error code: {response.status_code}")
    else:
        bot.send_message(message.chat.id, "😭 You are not in the channel. Unable to verify.")

if __name__ == "__main__":
    Thread(target=check_linked_users, daemon=True).start()
    bot.polling()
