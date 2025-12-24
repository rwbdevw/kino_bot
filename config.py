import os
from dotenv import load_dotenv

# Load .env file if present (for local development). On Render, variables come from the environment.
load_dotenv()

# Read secrets and IDs from environment variables.
# Fallbacks keep previous defaults to avoid breaking existing behavior if env vars are not set locally.
TOKEN = os.getenv('BOT_TOKEN', '')
admins = int(os.getenv('ADMINS', '6145787382'))
chat = int(os.getenv('CHAT_ID', '-1002382967806'))
POSTER_BASE_URL = os.getenv('POSTER_BASE_URL', 'https://bot.kinozzz.ru/poster/')

# Наш telegram канал - @End_Soft