from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
DATABASE_URL: str = os.getenv('DATABASE_URL')
ADMIN_ID: int = os.getenv('ADMIN_ID') or 1888872438

INLINE_QUERY_CACHE_TIME: int = os.getenv('INLINE_QUERY_CACHE_TIME') or 0

IMGBB_KEY: str = os.getenv('IMGBB_KEY')
