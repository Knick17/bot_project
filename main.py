import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

tmp = open('texts/meeting.txt', 'r', encoding='utf-8')

Meeting_text = tmp.read()

tmp.close()

# словарь для хранения информации о пользователях
answers = []

binary_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
binary_markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))

z_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
z_markup.add(types.KeyboardButton("Далее"))

f_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
f_markup.add(types.KeyboardButton("Человеческие фигуры"), types.KeyboardButton("Животные"),
               types.KeyboardButton("Неодушевленные предметы"), types.KeyboardButton("Что-либо фантастическое"))

t_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
t_markup.add(types.KeyboardButton("Всей целой картинки"), types.KeyboardButton("Только отдельной ее части"))

fou_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
fou_markup.add(types.KeyboardButton("Образ нечеткий и неяркий"),
                   types.KeyboardButton("Четко улавливается в первую очередь форма и в какой-то степени цвет"),
                   types.KeyboardButton("Четко улавливается в первую очередь цвет, а затем форма"))


# создаем обработчик для команды /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    answers.clear()
    bot.send_message(message.chat.id, Meeting_text.format(message.from_user.first_name), parse_mode='html',
                     reply_markup=binary_markup)
    bot.register_next_step_handler(message, zero_question)

# создаем обработчик для запроса роста пользователя
@bot.message_handler(commands=['text'])
def zero_question(message):
    if message.text == "/start":
        bot.register_next_step_handler(message, handle_start)
    elif message.text == "Нет":
        bot.stop_bot()
    elif message.text != "Да":
        bot.send_message(message.chat.id, "Не понимаю. Хотите начать?", parse_mode='html', reply_markup=binary_markup)
        bot.register_next_step_handler(message, zero_question)
    else:
        answers.append(message.text)

        bot.send_photo(message.chat.id, open(f'images/{len(answers) // 5 + 1}.jpg', 'rb'),
                       caption=f'{len(answers)}/50: Посмотрите внимательно на картинку-кляксу и подумайте, что вы видите: '
                               'кто или что это, где находится, что делает и т.д. '
                               'После того, как вы точно определитесь с наиболее близкой для себя '
                               'ассоциацией, ответьте на последующие вопросы.', reply_markup=f_markup)
        bot.register_next_step_handler(message, first_question)


@bot.message_handler(commands=['text'])
def first_question(message):
    if message.text == "/start":
        bot.register_next_step_handler(message, handle_start)
    elif message.text != "Далее":
        bot.send_message(message.chat.id, "Не понимаю. Попробуйте ещё раз", parse_mode='html', reply_markup=z_markup)
        bot.register_next_step_handler(message, first_question)
    else:
        chat_id = message.chat.id
        answers.append(message.text)
        bot.send_message(chat_id, f'{len(answers)}/50: Что вы видели на картинке?', reply_markup=f_markup)
        bot.register_next_step_handler(message, second_question)


@bot.message_handler(commands=['text'])
def second_question(message):
    if message.text == "/start":
        bot.register_next_step_handler(message, handle_start)
    elif message.text not in {"Человеческие фигуры", "Животные", "Что-либо фантастическое", "Неодушевленные предметы"}:
        bot.send_message(message.chat.id, "Не понимаю. Попробуйте ещё раз", parse_mode='html', reply_markup=f_markup)
        bot.register_next_step_handler(message, second_question)
    else:
        chat_id = message.chat.id
        answers.append(message.text)
        bot.send_message(chat_id, f'{len(answers)}/50: То, что вы видели на картинке, находилось в движении?',
                         reply_markup=binary_markup)

        bot.register_next_step_handler(message, third_question)


@bot.message_handler(commands=['text'])
def third_question(message):
    if message.text == "/start":
        bot.register_next_step_handler(message, handle_start)
    elif message.text not in {"Да", "Нет"}:
        bot.send_message(message.chat.id, "Не понимаю. Попробуйте ещё раз", parse_mode='html', reply_markup=binary_markup)
        bot.register_next_step_handler(message, third_question)
    else:

        chat_id = message.chat.id
        answers.append(message.text)

        bot.send_message(chat_id, f'{len(answers)}/50: Ваша ассоциация касается', reply_markup=t_markup)
        bot.register_next_step_handler(message, fourth_question)


@bot.message_handler(commands=['text'])
def fourth_question(message):
    if message.text == "/start":
        bot.register_next_step_handler(message, handle_start)
    elif message.text not in {"Всей целой картинки", "Только отдельной ее части"}:
        bot.send_message(message.chat.id, "Не понимаю. Попробуйте ещё раз", parse_mode='html', reply_markup=t_markup)
        bot.register_next_step_handler(message, fourth_question)
    else:
        chat_id = message.chat.id
        answers.append(message.text)

        bot.send_message(chat_id, f'{len(answers)}/50: Оцените, насколько получившийся образ оказался четким и ярким:',
                         reply_markup=fou_markup)
        if len(answers) >= 50:  # >= 50
            bot.register_next_step_handler(message, finish_registration)
        else:
            bot.register_next_step_handler(message, zero_question)

# создаем обработчик для завершения регистрации пользователя
def finish_registration(message):
    chat_id = message.chat.id
    answers.append(message.text)

    people = answers.count("Человеческие фигуры")
    animals = answers.count("Животные")
    subjects = answers.count("Неодушевленные предметы")
    fant = answers.count("Что-либо фантастическое")

    not_move = answers.count("Нет")

    part = answers.count("Только отдельной ее части")

    pure = answers.count("Образ нечеткий и неяркий")
    form = answers.count("Четко улавливается в первую очередь форма и в какой-то степени цвет")

    bot.send_message(chat_id, "Ваши ответы: \n", parse_mode='html', reply_markup=types.ReplyKeyboardRemove())

    tmp = open('texts/1.txt', 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format(people * 10, animals * 10, subjects * 10, fant * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()

    tmp = open('texts/3.txt', 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format((10 - not_move) * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()

    tmp = open('texts/4.txt', 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format((10 - part) * 10, part * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()

    tmp = open('texts/5.txt', 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format(pure * 10, form * 10, 100 - pure * 10 - form * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()


# запускаем бота
bot.polling(none_stop=True)
