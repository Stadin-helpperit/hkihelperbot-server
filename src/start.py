from dotenv import load_dotenv
from handlers import updater
import logging
import os

# --- RUN THIS TO TURN THE BOT ON ---

port = int(os.environ.get('PORT', 5000))
load_dotenv()
token = os.environ.get("API_TOKEN")


def main():
    # Logger, print's out info regarding bot's conversations
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # starts the polling of incoming messages
    updater.start_webhook(listen="0.0.0.0",
                          port=int(port),
                          url_path=token)
    updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + token)


if __name__ == "__main__":
    main()
