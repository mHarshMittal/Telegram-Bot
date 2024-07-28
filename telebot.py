import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import requests
import sys

class Reference:
    '''
    A class to store previously response from the Gemini AI API
    '''
    def __init__(self) -> None:
        self.response = ""

load_dotenv()

reference = Reference()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://api.gemini.ai/v1/response"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Tele Bot! Created by pwskills. How can I assist you?")

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a Telegram bot created by PWskills! Please follow these commands:
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help - to get this help menu
    I hope this helps. :)
    """
    await message.reply(help_command)

def get_gemini_response(prompt, previous_response):
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'previous_response': previous_response,
        'max_tokens': 50
    }
    response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)
    return response.json()['text']

@dispatcher.message_handler()
async def gemini_chat(message: types.Message):
    """
    A handler to process the user's input and generate a response using the Gemini AI API.
    """
    print(f">>> USER: \n\t{message.text}")
    response_text = get_gemini_response(message.text, reference.response)
    reference.response = response_text
    print(f">>> Gemini AI: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)
