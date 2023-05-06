import telebot
import config
from telebot import types
import texts.consts as consts

bot = telebot.TeleBot(config.TOKEN)

tmp = open(consts.MEET_PATH, 'r', encoding='utf-8')

Meeting_text = tmp.read()

tmp.close()

answers = []

binary_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
binary_markup.add(types.KeyboardButton(consts.YES), types.KeyboardButton(consts.NO))

z_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
z_markup.add(types.KeyboardButton(consts.NEXT))

f_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
f_markup.add(types.KeyboardButton(consts.HUMAN_BODIES), types.KeyboardButton(consts.ANIMALS),
             types.KeyboardButton(consts.OBJECTS), types.KeyboardButton(consts.FANTASTIC))

t_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
t_markup.add(types.KeyboardButton(consts.ALL_PIC), types.KeyboardButton(consts.PART_PIC))

fou_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
fou_markup.add(types.KeyboardButton(consts.NCLEAR_NVIVD),
               types.KeyboardButton(consts.FORM_COLOR),
               types.KeyboardButton(consts.COLOR_FORM))


# создаем обработчик для команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    answers.clear()
    bot.send_message(message.chat.id, Meeting_text.format(message.from_user.first_name), parse_mode='html',
                     reply_markup=binary_markup)
    bot.register_next_step_handler(message, zero_question)


@bot.message_handler(commands=['text'])
def zero_question(message):
    if message.text == consts.START:
        bot.register_next_step_handler(message, handle_start)
    elif len(answers) > 0 and message.text not in {consts.NCLEAR_NVIVD,
                                                   consts.FORM_COLOR,
                                                   consts.COLOR_FORM}:
        bot.send_message(message.chat.id, consts.NUNGERSTAND_TRY, parse_mode='html', reply_markup=fou_markup)
        bot.register_next_step_handler(message, zero_question)
    elif message.text == consts.NO and len(answers) == 0:
        bot.stop_bot()
    elif message.text != consts.YES and len(answers) == 0:
        bot.send_message(message.chat.id, consts.NUNDERSTAND_START, parse_mode='html', reply_markup=binary_markup)
        bot.register_next_step_handler(message, zero_question)
    else:
        answers.append(message.text)

        tmp = open(consts.IM_PATH.format(len(answers) // 5 + 1), 'rb')
        bot.send_photo(message.chat.id, tmp,
                       caption=consts.ZERO_QUESTION.format(len(answers)), reply_markup=z_markup)
        tmp.close()
        bot.register_next_step_handler(message, first_question)


@bot.message_handler(commands=['text'])
def first_question(message):
    if message.text == consts.START:
        bot.register_next_step_handler(message, handle_start)
    elif message.text != consts.NEXT:
        bot.send_message(message.chat.id, consts.NUNGERSTAND_TRY, parse_mode='html', reply_markup=z_markup)
        bot.register_next_step_handler(message, first_question)
    else:
        chat_id = message.chat.id
        answers.append(message.text)
        bot.send_message(chat_id, consts.FIRST_QUESTION.format(len(answers)), reply_markup=f_markup)
        bot.register_next_step_handler(message, second_question)


@bot.message_handler(commands=['text'])
def second_question(message):
    if message.text == consts.START:
        bot.register_next_step_handler(message, handle_start)
    elif message.text not in {consts.HUMAN_BODIES, consts.ANIMALS, consts.FANTASTIC, consts.OBJECTS}:
        bot.send_message(message.chat.id, consts.NUNGERSTAND_TRY, parse_mode='html', reply_markup=f_markup)
        bot.register_next_step_handler(message, second_question)
    else:
        chat_id = message.chat.id
        answers.append(message.text)
        bot.send_message(chat_id, consts.SECOND_QUESTION.format(len(answers)),
                         reply_markup=binary_markup)

        bot.register_next_step_handler(message, third_question)


@bot.message_handler(commands=['text'])
def third_question(message):
    if message.text == consts.START:
        bot.register_next_step_handler(message, handle_start)
    elif message.text not in {consts.YES, consts.NO}:
        bot.send_message(message.chat.id, consts.NUNGERSTAND_TRY, parse_mode='html', reply_markup=binary_markup)
        bot.register_next_step_handler(message, third_question)
    else:

        chat_id = message.chat.id
        answers.append(message.text)

        bot.send_message(chat_id, consts.THIRD_QUESTION.format(len(answers)), reply_markup=t_markup)
        bot.register_next_step_handler(message, fourth_question)


@bot.message_handler(commands=['text'])
def fourth_question(message):
    if message.text == consts.START:
        bot.register_next_step_handler(message, handle_start)
    elif message.text not in {consts.ALL_PIC, consts.PART_PIC}:
        bot.send_message(message.chat.id, consts.NUNGERSTAND_TRY, parse_mode='html', reply_markup=t_markup)
        bot.register_next_step_handler(message, fourth_question)
    else:
        chat_id = message.chat.id
        answers.append(message.text)

        bot.send_message(chat_id, consts.FORTH_QUESTION.format(len(answers)),
                         reply_markup=fou_markup)
        if len(answers) >= 50:  # >= 50
            bot.register_next_step_handler(message, finish_registration)
        else:
            bot.register_next_step_handler(message, zero_question)


def generate(answers):
    return (answers.count(consts.HUMAN_BODIES), answers.count(consts.ANIMALS),
            answers.count(consts.OBJECTS), answers.count(consts.FANTASTIC),
            answers.count(consts.NO),
            answers.count(consts.PART_PIC),
            answers.count(consts.NCLEAR_NVIVD),
            answers.count(consts.FORM_COLOR))


# создаем обработчик для завершения регистрации пользователя
def finish_registration(message):
    chat_id = message.chat.id
    answers.append(message.text)
    people, animals, subjects, fant, not_move, part, pure, form = generate(answers)

    bot.send_message(chat_id, consts.UR_ANSWERS, parse_mode='html', reply_markup=types.ReplyKeyboardRemove())

    tmp = open(consts.TXT_PATH.format(1), 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format(people * 10, animals * 10, subjects * 10, fant * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()

    tmp = open(consts.TXT_PATH.format(3), 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format((10 - not_move) * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()

    tmp = open(consts.TXT_PATH.format(4), 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format((10 - part) * 10, part * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()

    tmp = open(consts.TXT_PATH.format(5), 'r', encoding='utf-8')
    bot.send_message(chat_id, tmp.read().format(pure * 10, form * 10, 100 - pure * 10 - form * 10), parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    tmp.close()


# запускаем бота
bot.polling(none_stop=True)
