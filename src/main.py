

# --- THIS FILE IS THE INTERFACE BETWEEN OUR BOT AND GOOGLE DIALOGFLOW ---

from flask import Flask, request
import os
app = Flask(__name__)


@app.route('/')
def webhook():

    return "Hello"


if __name__ == '__main__':
    app.run(port='8000')
