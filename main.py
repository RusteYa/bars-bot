import telebot
import constants




bot = telebot.TeleBot(constants.TELEBOT_TOKEN)
telebot.apihelper.proxy = {'https': '35.231.54.121:8080'}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    all_files = {constants.photo1, constants.photo2, constants.photo3}
    user_markup.row('Я готов пройти опрос!')
    user_markup.row('/stop')
    bot.send_message(message.from_user.id, 'БАРС Груп приветствует тебя!', reply_markup=user_markup)
    for file in all_files:
        img = open(file, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img)
        img.close()

@bot.message_handler(content_types=['text'])
def handle_start(message):
    if message.text == "Я готов пройти опрос!":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        all_files = {constants.doc1}
        user_markup.row('Принять')
        user_markup.row('/stop')
        bot.send_message(message.from_user.id, 'Тогда прочитай и прими '
                                               'согласие на обработку персональных данных', reply_markup=user_markup)
        for file in all_files:
            doc = open(file, 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_document')
            bot.send_document(message.from_user.id, doc)
            doc.close()

bot.polling(none_stop=True, interval=0)
