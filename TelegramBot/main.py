# pip install python-telegram-bot
# pip install pandas-datareader
import telegram.ext
import pandas_datareader as web

def start(update, context):
    update.message.reply_text("Hello! Welcome to my Bot!")

def help(update, context):
    update.message.reply_text("""
    The following commands are available:

    /start -> Welcome message
    /help -> This message
    /content -> Information About Bot Content
    /contact -> Information About Contact
    /stock -> Information About Stock price, specify at second argument. i.e. /stock AAPL
    """)

def content(update, context):
    update.message.reply_text("Coming soon!")

def contact(update, context):
    update.message.reply_text("Currently living as a recluse!")

def handle_message(update, context):
    update.message.reply_text(f"You have said {update.message.text}")

def stock(message, context):
    ticker = context.args[0]
    try:
        data = web.DataReader(ticker, 'yahoo')
        price = data.iloc[-1]['Close']
        update.message.reply_text(f"Current price of {ticker} is {price:.2f}$!")
    except web._utils.RemoteDataError:
        update.message.reply_text(f"The stock {ticker} is not found.")

if __name__ == '__main__':

    # read token from https://web.telegram.org/z/
    # stored in a token.txt file for security

    with open('token.txt', 'r') as f:
        TOKEN = f.read()

    updater = telegram.ext.Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start", start))
    disp.add_handler(telegram.ext.CommandHandler("help", help))
    disp.add_handler(telegram.ext.CommandHandler("content", content))
    disp.add_handler(telegram.ext.CommandHandler("contact", contact))
    disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    disp.add_handler(telegram.ext.CommandHandler("stock", stock))

    updater.start_polling()
    updater.idle()
