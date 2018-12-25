import telebot
import constants

bot = telebot.TeleBot(constants.TELEBOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    all_files = {constants.photo1, constants.photo2, constants.photo3}
    user_markup.row('Я готов пройти опрос!')
    bot.send_message(message.from_user.id, 'БАРС Груп приветствует тебя!', reply_markup=user_markup)
    for file in all_files:
        img = open(file, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img)
        img.close()

@bot.message_handler(commands=['url'])
def handle_start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_my_site = telebot.types.InlineKeyboardButton(text='Наш сайт', url='https://life.bars.group/')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Узнай больше о нас, на сайте:  ", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_start(message):

    if message.text == ".net" or message.text == "Python" or message.text == "Другой язык":
        bot.send_message(message.from_user.id, 'Введите ФИО')
        bot.send_message(message.from_user.id, 'Введите телефон')
        bot.send_message(message.from_user.id, 'Введите почту')
        bot.send_message(message.from_user.id, 'Введите ВУЗ')
        bot.send_message(message.from_user.id, 'Введите курс')
        bot.send_message(message.from_user.id, 'Введите Факультет')

    if message.text == "Разработчик":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('.net')
        user_markup.row('Python')
        user_markup.row('Другой язык')
        bot.send_message(message.from_user.id, 'Выбери язык',
                         reply_markup=user_markup)

    if message.text == "Принять":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Разработчик')
        user_markup.row('Аналитик')
        user_markup.row('Другое')
        bot.send_message(message.from_user.id, 'Хочешь попасть к нам в команду? Заполни анкету!', reply_markup=user_markup)
        bot.send_message(message.from_user.id, 'Кем хочешь работать?', reply_markup=user_markup)

    if message.text == "Я готов пройти опрос!":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        all_files = {constants.doc1}
        user_markup.row('Принять')
        bot.send_message(message.from_user.id, 'Тогда прочитай и прими '
                                               'согласие на обработку персональных данных', reply_markup=user_markup)
        for file in all_files:
            doc = open(file, 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_document')
            bot.send_document(message.from_user.id, doc)
            doc.close()

@bot.message_handler(content_types=['text'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/url')
    bot.send_message(message.from_user.id, 'Введите ФИО', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Введите телефон', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Введите почту', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Введите ВУЗ', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Введите курс', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Введите Факультет', reply_markup=user_markup)

bot.polling(none_stop=True, interval=0)
