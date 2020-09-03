import telegram, os, logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Loads the api token from the .env file
load_dotenv()

# Logger, print's out info in case something is going wrong
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Creating an Updater object, continously fetches new updates from Telegram
updater = Updater(token=os.environ.get("API_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


# --- HERE WE DEFINE DIFFERENT FUNCTIONS THAT SEND MESSAGES ---

# Function that sends a message ""I'm a bot, please talk to me!""
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


# Function that echoes the user's messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Function that sends the given text back in all caps as a message
def caps(update, context):
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# --- HERE WE CREATE HANDLER TYPE OBJECTS THAT LISTEN FOR COMMAND AND CALL THE DESIRED FUNCTIONS ---

# This handler listens for the command "/start" and calls the previously defined
# start function
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# This handler listens for the command "/start" and calls the previously defined caps function
caps_handler = CommandHandler("caps", caps)
dispatcher.add_handler(caps_handler)

# This handler listens for user's messages and calls the previously defined echo function
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# starts the polling of messages
updater.start_polling()
