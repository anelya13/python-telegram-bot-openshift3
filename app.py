import logging
import random
from queue import Queue
from threading import Thread
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '783982541:AAEBU1m5fRplBfcNFozSMLoOTwO5HzIFXCI'


def open(bot, update):
    """Send a message when the command /start is issued."""
    """update.message.reply_text('Welcome to the Test Bot! I will reply you what you will write me.')"""
    bot.send_message(chat_id=update.message.chat_id,
                     text='<b>Библиотека КАЗГЮУ </b>,<a href="http://kazguu.kz/ru/">Библиотека</a>', parse_mode=ParseMode.HTML)



def help(bot, update):
    """Send a message when the command /help is issued."""
    # update.message.reply_text('You can get any help here.')

    keyboardButtons = [[InlineKeyboardButton("Помощь", callback_data="1")],
                       [InlineKeyboardButton("Примеры", callback_data="2")],
                       [InlineKeyboardButton("Ссылка", url="http://google.com")]]
    keyboard = InlineKeyboardMarkup(keyboardButtons)
    update.message.reply_text('Сделайте выбор:', reply_markup=keyboard)


def button(bot, update):
    query = update.callback_query
    if query.data == "1":
        text = "Song 1"
    elif query.data == "2":
        text = "3+4, 44-12, 43/2, 12*90"
    bot.editMessageText(text=text, chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)  # Create the EventHandler and pass it your bot's token.
        bot = updater.bot
        dp = updater.dispatcher  # Get the dispatcher to register handlers
        dp.add_handler(CommandHandler("open", open))  # on /start command answer in Telegram
        dp.add_handler(CommandHandler("help", help))  # on /help command answer in Telegram
        dp.add_handler(CallbackQueryHandler(button))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()  # Start the Bot
        """Run the bot until you press Ctrl-C or the process receives SIGINT,
        SIGTERM or SIGABRT. This should be used most of the time, since
        start_polling() is non-blocking and will stop the bot gracefully."""
        updater.idle()


if __name__ == '__main__':
    setup()
