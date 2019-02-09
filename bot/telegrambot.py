import logging

from django_telegrambot.apps import DjangoTelegramBot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from bot import constants, google_sheet
from bot.models import User, Question, Answer, Choices

logger = logging.getLogger(__name__)


def get_user(chat_id):
    users = User.objects.filter(chat_id=chat_id)
    return users.__getitem__(0)


def save_speciality(message, speciality):
    user = get_user(message.chat.id)
    user.specialty = speciality
    user.save()


def start(bot, update):
    message = update.message
    print(message.chat.id, message.chat.first_name, message.chat.last_name)

    if User.objects.filter(chat_id=message.chat_id).__len__() == 0:
        user = User(chat_id=message.chat.id,
                    first_name=message.chat.first_name,
                    last_name=message.chat.last_name)
        user.save()
    else:
        current_user = User.objects.filter(chat_id=message.chat_id).first()
        Answer.objects.filter(user=current_user).delete()
        current_user.current_question = None

    print("User logined")

    all_files = {constants.photo1, constants.photo2, constants.photo3}
    user_markup = [['Я готов пройти опрос!']]
    update.message.reply_text('БАРС Груп приветствует тебя!',
                              reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
    for file in all_files:
        img = open(file, 'rb')
        bot.send_photo(update.message.chat_id, img)
        img.close()


def url(bot, update):
    update.message.reply_text("Спасибо за прохождение опроса!", reply_markup=ReplyKeyboardRemove())
    user_markup = [[InlineKeyboardButton(text='Наш сайт', url='https://life.bars.group/')]]
    update.message.reply_text("Узнай больше о нас, на сайте:  ",
                              reply_markup=InlineKeyboardMarkup(user_markup, one_time_keyboard=True))
    google_sheet.send_to_google_sheet(get_user(update.message.chat.id))
    return ConversationHandler.END


def echo(bot, update):
    message = update.message
    user = get_user(message.chat.id)
    text = message.text
    # question = user.__getattribute__('current_question')

    if message.text == "Я готов пройти опрос!":
        user_markup = [['Принять']]
        all_files = {constants.doc1}
        message.reply_text('Тогда прочитай и прими согласие на обработку персональных данных',
                           reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
        for file in all_files:
            doc = open(file, 'rb')
            bot.send_document(message.chat_id, doc)
            doc.close()

    if message.text == "Принять":
        message.reply_text('Хочешь попасть к нам в команду? Заполни анкету!')
        # user_markup = [['Разработчик', 'Аналитик', 'Другая специальность']]
        # message.reply_text('Кем хочешь работать?',
        #                    reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
        next_question = Question.objects.filter(is_start_question=True).first()
        if next_question is not None:
            user.current_question = next_question
            user.save()
            answers_query_set = Choices.objects.filter(question=next_question)
            if next_question.have_choices:
                user_markup = [list(map(lambda answer: answer.text, answers_query_set))]
                message.reply_text(next_question.text,
                                    reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
            else:
                message.reply_text(next_question.text)
        else:
            url(bot, update)

    question = user.current_question
    if question is not None:
        if question.have_choices:
            next_question = Choices.objects.filter(text=text).first().next_question
        else:
            next_question = question.next

        answer = Answer.objects.all().filter(question=question, user=user).first()
        if answer is None:
            answer = Answer(question=question, user=user)
        answer.text = text
        answer.save()

        if next_question is not None:
            user.current_question = next_question
            user.save()
            answers_query_set = Choices.objects.filter(question=next_question)

            if next_question.have_choices:
                user_markup = [list(map(lambda answer: answer.text, answers_query_set))]
                message.reply_text(next_question.text,
                                   reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))
            else:
                message.reply_text(next_question.text)
        else:
            url(bot, update)

    # if question == 'schedule':
    #     user.schedule = text
    #     user.question = 'schedule'
    #     user.save()
    #     url(bot, update)
    #
    # if question == 'time_work':
    #     user.time_work = text
    #     user.question = 'schedule'
    #     user.save()
    #     message.reply_text('Удобный график работы?')
    #
    # if question == 'skills':
    #     user.skills = text
    #     user.question = 'time_work'
    #     user.save()
    #     message.reply_text('Когда готовы приступить к работе?')
    #
    # if question == 'study':
    #     user.study = text
    #     user.question = 'skills'
    #     user.save()
    #     message.reply_text('Укажите ключевые ИТ навыки:')
    #
    # if question == 'email':
    #     user.email = text
    #     user.question = 'study'
    #     user.save()
    #     message.reply_text('Введите место учебы (ВУЗ, курс и факультет)')
    #
    # if question == 'phone':
    #     user.phone = text
    #     user.question = 'email'
    #     user.save()
    #     message.reply_text('Введите почту')
    #
    # if question == 'fio':
    #     user.fio = text
    #     user.save()
    #     user.question = 'phone'
    #     message.reply_text('Введите телефон')
    #
    # if question == 'Введите Вашу специальность':
    #     user.question = 'fio'
    #     user.save()
    #     save_speciality(message, message.text)
    #     message.reply_text('Введите ФИО')
    #
    # if question == 'На каких языках Вы программируете?':
    #     user.programm_language = text
    #     user.save()
    #
    # if question == 'fio':
    #     user.fio = text
    #     user.save()
    #
    # if text == ".net" or text == "Python":
    #     user.programm_language = text
    #     user.question = 'fio'
    #     user.save()
    #     message.reply_text('Введите ФИО')
    #
    # if text == "Аналитик":
    #     user.question = 'fio'
    #     user.specialty = 'Аналитик'
    #     user.save()
    #     message.reply_text('Введите ФИО')
    #
    # if text == "Другое":
    #     user.question = 'На каких языках Вы программируете?'
    #     user.save()
    #     message.reply_text(user.question)
    #
    # if text == "Другая специальность":
    #     user.question = 'Введите Вашу специальность'
    #     user.save()
    #     message.reply_text('Введите Вашу специальность')
    #
    # if message.text == "Разработчик":
    #     save_speciality(message, "Разработчик")
    #     user_markup = [['.net', 'Python', 'Другое']]
    #     message.reply_text('Выбери язык',
    #                        reply_markup=ReplyKeyboardMarkup(user_markup, one_time_keyboard=True))


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
