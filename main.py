import telebot
import config
import random

from telebot import types

Meeting_text = "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы провести тест Роршаха." \
               "\n\n" \
               "С тестом Роршаха, который представляет собой картинки в виде чернильных пятен знакомы многие, как минимум из фильмов и различных передач. А вот пройти его и узнать о себе что-то новое доводилось не каждому. Сейчас мы попробуем исправить это упущение. Специально для вас мы подготовили базовую реализацию онлайн теста Роршаха, с помощью которой вы сможете узнать себя с новой стороны." \
               "Но не стоит забывать, что составить полную картину и использовать весь потенциал пятен Роршаха может только специалист при личной беседе.Что от вас потребуется? Внимательно, не торопясь, посмотреть на картинку с пятном. Представить, что или кого вы увидели, что оно делает. После того, как у вас сформировался полный образ ассоциации, ответьте на несколько вопросов. Готовы пройти тест Роршаха? Приступим?"

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    # sti = open('static/welcome.webp', 'rb')
    # bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Да")
    item2 = types.KeyboardButton("Нет")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     Meeting_text.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Да':
            bot.send_message(message.chat.id, "Поехали, " + str(random.randint(0, 100)))
        elif message.text == 'Нет':
            bot.send_message(message.chat.id, 'До свидания')
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить')


# RUN
bot.polling(none_stop=True)
bot.polling(none_stop=True)
