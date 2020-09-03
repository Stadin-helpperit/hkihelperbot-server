import telegram, os
from dotenv import load_dotenv

load_dotenv()

bot = telegram.Bot(token=os.environ.get("API_TOKEN"))

print(bot.get_me())
