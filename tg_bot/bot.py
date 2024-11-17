import ast
import os
import random
import sqlite3
import string
import sys

import django
from asgiref.sync import sync_to_async
from django.utils.crypto import get_random_string
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Add your project’s root directory to the Python path
sys.path.append(r"your root of project path")

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_game_mini_app.settings")

# Initialize Django
django.setup()

from authentication.models import Referral, User, UserPasswords

bot = Client(
    "quiz mini app",
    "your api id",
    "your api hash",
    bot_token="YOUR_BOT_TOKEN"
)

# Connect to SQLite database
conn = sqlite3.connect("../db.sqlite3")
cursor = conn.cursor()


def generate_random_string(length=10):
    """Generate a random alphanumeric string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    url = WebAppInfo(url="your ssl certificate host")
    keys = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("mini app", web_app=url)
        ]
    ])
    # Wrap each operation in sync_to_async
    ref_qs = await sync_to_async(Referral.objects.filter, thread_sensitive=True)(id=message.chat.id)

    # Check if user exists in referral (async)
    referral__user_exists = await sync_to_async(ref_qs.exists, thread_sensitive=True)()
    if referral__user_exists:
        await message.reply("Welcome Back 🌷", reply_markup=keys)

    # Check if there's an argument after /start
    elif len(message.command) > 1:
        referral_id = message.command[1]  # Get the referral code after /start

        # Wrap each operation in sync_to_async
        referral_qs = await sync_to_async(Referral.objects.filter, thread_sensitive=True)(id=referral_id)

        # Check if the referral exists (async)
        referral_exists = await sync_to_async(referral_qs.exists, thread_sensitive=True)()

        if referral_exists:
            # Get the referral instance (async)
            referral = await sync_to_async(referral_qs.first, thread_sensitive=True)()

            # Convert referred_users string to list if it's a valid list, otherwise use an empty list
            referred_users = ast.literal_eval(referral.referred_users) if referral.referred_users else []

            # Check if the user has already been referred
            if message.chat.id not in referred_users:
                referred_users.append(message.chat.id)

                # Convert the list back to a string to store in the database
                referral.referred_users = str(referred_users)
                await sync_to_async(referral.save, thread_sensitive=True)()

            # Generate a unique username
            username = message.chat.username if message.chat.username else \
                f"{message.chat.first_name}_{generate_random_string()}"

            # Generate a strong password and store it
            password = get_random_string(12)  # Generate a secure 12-character password

            # Create the new user
            new_user = await sync_to_async(User.objects.create_user)(
                username=username,
                first_name=message.chat.first_name,
                is_active=True,
                level=0
            )

            # Set the password for the new user (async)
            await sync_to_async(new_user.set_password)(password)
            await sync_to_async(new_user.save)()

            # Create a new referral record for this user
            await sync_to_async(Referral.objects.create)(
                id=message.chat.id,
                user_id=new_user.id
            )

            # Store the password in the UserPasswords table with the Telegram ID as user_id
            await sync_to_async(UserPasswords.objects.create)(
                user_id=message.chat.id,
                password=password
            )

            await message.reply(f"Welcome! You were referred by ID: {referral_id}", reply_markup=keys)
        else:
            # If the referral ID is invalid
            button = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Join Channel", url="https://t.me/test_channel")]
                ]
            )
            await message.reply(
                "Hey, this referral ID is invalid. Please go to our channel to pick a valid referral code.",
                reply_markup=button
            )


bot.run()
