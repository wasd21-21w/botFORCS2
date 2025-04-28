
import sqlite3
from telebot import types
import telebot
bot = telebot.TeleBot('7976911373:AAHiZVtSBT14TlyLAh7GHDhBtXHDANsB0sc')
user_data = {}

questions = ['Как вас зовут?',
             'Сколько вам лет?',
             'Проведенного времени (ч) в кс?',
             'На сколько бы вы оценили ваши навыки игры - (0/10)',
             ]
ADMIN_ID = 929599878
#старт
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {'step': 0, 'answers': []}
    markup = types.InlineKeyboardMarkup()
    b = types.InlineKeyboardButton("Анкета", callback_data='Анкета')
    markup.add(b)
    bot.send_photo(message.chat.id,f'https://imgur.com/a/5i7TUi0', f'Привет - {message.chat.username}' 
                   f'\nРады, что ты решил принять участие в турнире'
                   f'\nДля дальнейшего продвижения, нам нужно оценить твои навыки'
                   f'\nПредлагаем {message.chat.first_name} - заполнить анкету', reply_markup=markup)

#обработка ответов
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def question(message):
    user = user_data[message.chat.id]
    step = user['step']
    user['answers'].append(message.text)

    step+=1
    if step < len(questions):
        user['step'] = step
        bot.send_message(message.chat.id, questions[step])

    else:
        # анкета заполнена
        summary = "\n".join(f"{questions[i]} {user['answers'][i]}" for i in range(len(questions)))
        bot.send_message(message.chat.id, "Спасибо! Ваша анкета отправлена.")
        bot.send_message(ADMIN_ID,
                         f"Новая анкета от @{message.from_user.username or message.from_user.first_name}:\n\n{summary}")
        del user_data[message.chat.id]
#обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def anketa(call):
    if call.data == 'Анкета':
        bot.send_message(call.message.chat.id, questions[0])
bot.polling(none_stop=True)

