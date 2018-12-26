import logging

from django_telegrambot.apps import DjangoTelegramBot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from bot import constants

logger = logging.getLogger(__name__)


def start(bot, update):
    all_files = {constants.photo1, constants.photo2, constants.photo3}
    user_markup = [['Я готов пройти опрос!']]
    update.message.reply_text('БАРС Груп приветствует тебя!',
                              reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
    for file in all_files:
        img = open(file, 'rb')
        bot.send_photo(update.message.chat_id, img)
        img.close()


def url(bot, update):
    user_markup = [[InlineKeyboardButton(text='Наш сайт', url='https://life.bars.group/')]]
    update.message.reply_text("Узнай больше о нас, на сайте:  ",
                              reply_markup=InlineKeyboardMarkup(user_markup, one_time_keyboard=True))


def echo(bot, update):
    if update.message.text == ".net" or update.message.text == "Python" or update.message.text == "Другой язык":
        update.message.reply_text('Введите ФИО')
        update.message.reply_text('Введите телефон')
        update.message.reply_text('Введите почту')
        update.message.reply_text('Введите ВУЗ')
        update.message.reply_text('Введите курс')
        update.message.reply_text('Введите Факультет')

    if update.message.text == "Разработчик":
        user_markup = [['.net', 'Python', 'Другой язык']]
        update.message.reply_text('Выбери язык',
                                  reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))

    if update.message.text == "Принять":
        user_markup = [['Разработчик', 'Аналитик', 'Другое']]

        update.message.reply_text('Хочешь попасть к нам в команду? Заполни анкету!',
                                  reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
        update.message.reply_text('Кем хочешь работать?',
                                  reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))

    if update.message.text == "Я готов пройти опрос!":
        user_markup = [['Принять']]
        all_files = {constants.doc1}
        update.message.reply_text('Тогда прочитай и прими согласие на обработку персональных данных',
                                  reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
        for file in all_files:
            doc = open(file, 'rb')
            bot.send_document(update.message.chat_id, doc)
            doc.close()


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Cancel',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    logger.info("Loading handlers for telegram bot")

    dp = DjangoTelegramBot.dispatcher

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #
    #     states={
    #     },
    #
    #     fallbacks=[CommandHandler('cancel', cancel)]
    # )
    dp.add_handler(CommandHandler('url', url))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('cancel', cancel))
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
