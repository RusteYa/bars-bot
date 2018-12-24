import os
from datetime import datetime
import telebot

import constants

bot = telebot.TeleBot(constants.TELEBOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/stop')
    user_markup.row('Photo', 'Audio', 'Document')
    user_markup.row('Sticker', 'Video', 'Voice', 'Location')
    bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Photo':
        directory = 'C:/Users/user/Desktop/t_bot/templates/Photos'
        all_files_in_directory = os.listdir(directory)
        print(all_files_in_directory)
        for file in all_files_in_directory:
            img = open(directory + '/' + file, 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img)
            img.close()

bot.polling(none_stop=True, interval=0)

# upd = bot.get_updates()
#
# last_upd = upd[-1]
# message_from_user = last_upd.message
# print(message_from_user)
#
# def log(message, answer):
#     print("\n ----------")
#     print(datetime.now())
#     print("Message from {0} {1}. (id = {2}) \n Text - {3}".format(message.from_user.first_name,
#                                                                   message.from_user.last_name,
#                                                                   str(message.from_user.id),
#                                                                   message.text))
#     print(answer)
#
# @bot.message_handler(commands=['start'])
# def handle_com(message):
#     bot.send_message(message.chat.id, "БАРС Груп приветствует тебя!")
#
# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     answer = "Yes"
#     if message.text == "A":
#         answer = "B"
#         log(message, answer)
#         bot.send_message(message.chat.id, "B")
#     elif message.text == "B":
#         answer = "C"
#         bot.send_message(message.chat.id, "C")
#         log(message, answer)
#     else:
#         bot.send_message(message.chat.id, answer)
#         log(message, answer)
#
#
# bot.polling(none_stop=True, interval=0)

# USERS = {
#     152922019: {}
# }

# @bot.message_handler(commands=['start', 'help'])
# def command_handler(message: Message):
#     bot.reply_to(message, "БАРС Груп приветствует тебя!")
#
# @bot.message_handler(content_types=['text'])
# @bot.edited_message_handler(content_types=['text'])
# def echo_digits(message: Message):
#     if 'Hi' in message.text:
#         bot.reply_to(message, 'Hi there')
#         return
#
# @bot.message_handler(content_types=['sticker'])
# def sticker_handler(message:Message):
#     bot.send_sticker(message.chat.id, constants.STICKER_ID)
#
# bot.polling(timeout=60)