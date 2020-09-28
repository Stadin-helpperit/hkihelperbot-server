from src.handlers import updater
import logging

# --- RUN THIS TO TURN THE BOT ON ---


def main():
    # Logger, print's out info regarding bot's conversations
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # starts the polling of incoming messages
    updater.start_polling()

    if __name__ == "__main__":
        main()
