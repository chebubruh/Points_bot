from telebot import *
import config
import main

bot = TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    main.create_students(message.chat.first_name.lower())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    a1 = types.KeyboardButton(text='Общетеоретические дисциплины')
    a2 = types.KeyboardButton(text='Цивилистические дисциплины')
    a3 = types.KeyboardButton(text='Земельное право')
    a4 = types.KeyboardButton(text='Природоресурсное право')
    a5 = types.KeyboardButton(text='Предпринимательское право')
    a6 = types.KeyboardButton(text='Судебное делопроизводство')
    a7 = types.KeyboardButton(text='СудебноЭкспертная деятельность')
    keyboard.add(a1, a2, a3, a4, a5, a6, a7)
    bot.send_message(message.chat.id, 'Здарова мудень, я буду следить за твоими баллами', reply_markup=keyboard)


@bot.message_handler(commands=['clear'])
def _(message):
    main.clear(message.chat.first_name.lower())
    bot.send_message(message.chat.id, 'Все баллы, полученные за сегодняшний день удалены')


@bot.message_handler(commands=['score'])
def _(message):
    bot.send_message(message.chat.id, main.all_points(message.chat.first_name.lower()))


@bot.message_handler(content_types=['text'])
def choice(message):
    for i in main.subjects:
        if message.text.split()[0] in i:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            answer = types.InlineKeyboardButton('Ответ', callback_data='btn1')
            dlc = types.InlineKeyboardButton('Дополнение', callback_data='btn2')
            check = types.InlineKeyboardButton('Сумма баллов', callback_data='btn3')
            table = types.InlineKeyboardButton('Даты баллов', callback_data='btn4')
            keyboard.add(answer, dlc, check, table)
            bot.send_message(message.chat.id, message.text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_info(callback):
    if callback.message.text == 'Общетеоретические дисциплины':
        callback.message.text = 'Общетеоретические_дисциплины'
    elif callback.message.text == 'Цивилистические дисциплины':
        callback.message.text = 'Цивилистические_дисциплины'
    elif callback.message.text == 'Земельное право':
        callback.message.text = 'Земельное_право'
    elif callback.message.text == 'Природоресурсное право':
        callback.message.text = 'Природоресурсное_право'
    elif callback.message.text == 'Предпринимательское право':
        callback.message.text = 'Предпринимательское_право'
    elif callback.message.text == 'Судебное делопроизводство':
        callback.message.text = 'Судебное_делопроизводство'
    elif callback.message.text == 'СудебноЭкспертная деятельность':
        callback.message.text = 'СудебноЭкспертная_деятельность'

    if callback.data == 'btn1':
        if main.add_points(callback.message.text, callback.message.chat.first_name.lower(),
                           True) != 'кого ты обманываешь? товой максимум - это 1 ответ за семинар':
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text=f'закинул <b>ОТВЕТ</b> в копилочку по предмету - "{callback.message.text}"',
                                  parse_mode='HTML')
        else:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='кого ты обманываешь? товой максимум - это 1 ответ за семинар')

    elif callback.data == 'btn2':
        main.add_points(callback.message.text, callback.message.chat.first_name.lower(), False)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text=f'закинул <b>ДОПОЛНЕНИЕ</b> в копилочку по предмету "{callback.message.text}"',
                              parse_mode='HTML')

    elif callback.data == 'btn3':
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text=main.total_points(callback.message.text, callback.message.chat.first_name.lower()))

    elif callback.data == 'btn4':
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text=main.view_table(callback.message.text, callback.message.chat.first_name.lower()))


bot.polling(True)
