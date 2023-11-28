import telebot
import random
import sqlite3
import time

# Замените 'YOUR_BOT_TOKEN' на ваш токен
bot = telebot.TeleBot('YOUR_BOT_TOKEN')


movie_codes = ["#{}".format(str(code).zfill(4)) for code in range(1111, 1201)]

channel_links = {
    "Название канала": "https://t.me/ссылка на телеграм канал",
    "Название канала": "https://t.me/ссылка на телеграм канал",
    "Название канала": "https://t.me/ссылка на телеграм канал"
}

# Создание и подключение к базе данных
conn = sqlite3.connect('free_spins.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для хранения информации о пользователях и фриспинах
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        username TEXT
    )
''')
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    chat_id = message.chat.id
    cursor.execute('INSERT OR IGNORE INTO users (chat_id, username) VALUES (?, ?)',
                   (chat_id, username))
    conn.commit()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Продолжить"))
    bot.send_message(chat_id, f"Добро пожаловать в телеграмм КиноПоиск,\n"
                              f"{username}!",reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == "Продолжить")
def continue_button(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Найти фильм по коду ✅"))
    markup.add(telebot.types.KeyboardButton("Случайный фильм ✅"))
    bot.send_message(message.chat.id, "Тут ты можешь искать лучшие фильмы по коду или жанру, так как у нас огромная база с более чем 200 фильмов.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Найти фильм по коду ✅")
def spin_button(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "Введите код фильма: \n"
                                      "Пример '#3143'",
                     reply_markup=markup)
    bot.register_next_step_handler(message, process_info)

@bot.message_handler(func=lambda message: message.text == "Случайный фильм ✅")
def spin_button(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "Введите код фильма: \n"
                                      "Пример '#3143'",
                     reply_markup=markup)
    bot.register_next_step_handler(message, process_info)



def process_info(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    subscribe_button = telebot.types.KeyboardButton(" ✅Подписался/-лась ✅")
    markup.add(subscribe_button)
    channels_markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for channel_name, channel_link in channel_links.items():
        channel_button = telebot.types.InlineKeyboardButton(channel_name, url=channel_link)
        channels_markup.add(channel_button)

    bot.send_message(message.chat.id, "‼️Что бы искать фильм, сначала нужно подписаться на следующие каналы:‼️\n",
                     reply_markup=channels_markup)
    bot.send_message(message.chat.id, "И так же пригласить в этого бота хотя бы одного  \n"
                                      "‼️ВАЖНО оставаться подписанным на каналы‼️", reply_markup=markup)

def subscribed(message):
    required_channels = [
        "-1001785132543", # Channel ID 1
        "-1001636042770", # Channel ID 2
        "-1001823416637", # Channel ID 3

    ]

    user_id = message.chat.id
    user_channels = [channel_id for channel_id in required_channels if is_member(user_id, channel_id)]

    if len(user_channels) == len(required_channels):
        bot.send_message(user_id,
                         "Отлично!\n"
                         "\n"
                         "Теперь вы можете пользоваться всем функционалом✅")
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        subscribe_button = telebot.types.KeyboardButton("✅Подписался/-лась ✅")
        markup.add(subscribe_button)
        bot.send_message(user_id, "‼️Ты не подписался‼️", reply_markup=markup)


def is_member(user_id, channel_id):
    member_status = bot.get_chat_member(chat_id=channel_id, user_id=user_id).status
    return member_status in ['creator', 'administrator', 'member']


@bot.message_handler(func=lambda message: message.text == "✅Подписался/-лась ✅")
def subscribed_handler(message):
    subscribed(message)
    continue_button2(message)



def continue_button2(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Найти фильм по коду✅"))
    markup.add(telebot.types.KeyboardButton("Случайный фильм✅"))
    bot.send_message(message.chat.id, "Тут ты можешь искать лучшие фильмы по коду или жанру, так как у нас огромная база с более чем 200 фильмов.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Найти фильм по коду✅")
def findfilm(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "Введите код фильма: \n"
                                      "Пример '#2211'",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Случайный фильм✅")
def find_random_film(message):
    random_movie_code = random.choice(movie_codes)

    # Retrieve movie information based on the random code
    if random_movie_code == "#1111":
        filmBredPit1(message)
    elif random_movie_code == "#1112":
        filmBredPit2(message)
    elif random_movie_code == "#1113":
        filmBredPit3(message)
    elif random_movie_code == "#1114":
        filmBredPit4(message)
    elif random_movie_code == "#1115":
        filmBredPit6(message)
    elif random_movie_code == "#1117":
        filmBredPit7(message)
    elif random_movie_code == "#1118":
        filmBredPit8(message)
    elif random_movie_code == "#1119":
        filmBredPit9(message)
    elif random_movie_code == "#1120":
        filmBredPit10(message)
    elif random_movie_code == "#1120":
        richard_gere3(message)
    elif random_movie_code == "#1121":
        richard_gere4(message)
    elif random_movie_code == "#1122":
        richard_gere5(message)
    elif random_movie_code == "#1123":
        richard_gere8(message)

    elif random_movie_code == "#1124":
        richard_gere10(message)
    elif random_movie_code == "#1125":
        johnny_depp1(message)
    elif random_movie_code == "#1126":
        johnny_depp2(message)
        # Continue adding cases for other movie codes up to #1200
    elif random_movie_code == "#1127":
        johnny_depp3(message)
    elif random_movie_code == "#1128":
        johnny_depp4(message)
    elif random_movie_code == "#1129":
        johnny_depp5(message)
    elif random_movie_code == "#1130":
        johnny_depp6(message)
    elif random_movie_code == "#1131":
        johnny_depp8(message)
    elif random_movie_code == "#1132":
        tom_hardy1(message)


    elif random_movie_code == "#1133":
        tom_hardy3(message)
    elif random_movie_code == "#1134":
        tom_hardy5(message)
    elif random_movie_code == "#1135":
        tom_hardy6(message)
    elif random_movie_code == "#1136":
        tom_hardy7(message)
    elif random_movie_code == "#1137":
        tom_hardy10(message)


    elif random_movie_code == "#1138":
        will_smith1(message)
    elif random_movie_code == "#1139":
        will_smith2(message)
    elif random_movie_code == "#1140":
        will_smith3(message)
    elif random_movie_code == "#1141":
        will_smith4(message)
    elif random_movie_code == "#1142":
        will_smith5(message)
    elif random_movie_code == "#1143":
        will_smith6(message)
    elif random_movie_code == "#1144":
        will_smith7(message)
    elif random_movie_code == "#1145":
        will_smith8(message)
    elif random_movie_code == "#1146":
        will_smith9(message)
    elif random_movie_code == "#1147":
        will_smith10(message)


    elif random_movie_code == "#1148":
        mark_wahlberg1(message)
    elif random_movie_code == "#1149":
        mark_wahlberg2(message)
    elif random_movie_code == "#1150":
        mark_wahlberg3(message)
    elif random_movie_code == "#1151":
        mark_wahlberg4(message)
    elif random_movie_code == "#1152":
        mark_wahlberg5(message)
    elif random_movie_code == "#1153":
        mark_wahlberg6(message)
    elif random_movie_code == "#1154":
        mark_wahlberg8(message)
    elif random_movie_code == "#1155":
        mark_wahlberg9(message)


    elif random_movie_code == "#1156":
        channing_tatum2(message)
    elif random_movie_code == "#1157":
        channing_tatum3(message)
    elif random_movie_code == "#1158":
        channing_tatum4(message)
    elif random_movie_code == "#1159":
        channing_tatum6(message)
    elif random_movie_code == "#1160":
        channing_tatum7(message)
    elif random_movie_code == "#1161":
        channing_tatum8(message)
    elif random_movie_code == "#1162":
        channing_tatum9(message)
    elif random_movie_code == "#1163":
        channing_tatum10(message)


    elif random_movie_code == "#1164":
        jim_carrey3(message)
    elif random_movie_code == "#1165":
        jim_carrey4(message)
    elif random_movie_code == "#1166":
        jim_carrey5(message)
    elif random_movie_code == "#1167":
        jim_carrey6(message)
    elif random_movie_code == "#1168":
        jim_carrey7(message)
    elif random_movie_code == "#1169":
        jim_carrey9(message)

    elif random_movie_code == "#1170":
        jim_carrey10(message)






#===========================================================================================================================================================================================================================================================================
@bot.message_handler(func=lambda message: message.text == "#1111")
def filmBredPit1(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Бойцовский клуб \n"\
                                      "Жанр: Драма, триллер \n"\
                                      "Страна: США, 1999 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/thumb/8/8a/Fight_club.jpg/210px-Fight_club.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1112")
def filmBredPit2(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Заводной апельсин \n" \
                 "Жанр: Драма, криминал, научная фантастика \n" \
                 "Страна: Великобритания, 1971 \n" \
                 "\n" \
                 "Приятного просмотра"

    # Отправка фотографии (замените 'photo_url' на реальный URL изображения)
    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/thumb/d/db/Clockwork_orange_ver2.jpg/227px-Clockwork_orange_ver2.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1113")
def filmBredPit3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =    "Название: Семь \n"\
                    "Жанр: Детектив, триллер \n"\
                    "Страна: США, 1995 \n"\
                                      "\n"\
                    "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/8/83/Se7en_%28poster%29.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1114")
def filmBredPit4(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Убить Билла: Вторая часть \n"\
                                      "Жанр: Экшн, криминал, триллер \n"\
                                      "Страна: США, 2004 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://s6.vcdn.biz/static/f/3091348491/image.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1115")
def filmBredPit6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Кролик Джоджо \n"\
                                      "Жанр: Драма, военный, комедия \n"\
                                      "Страна: США, 2019 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/a/a3/Jojo_Rabbit.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1116")
def filmBredPit7(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Мистер и миссис Смит \n"\
                                      "Жанр: Экшн, комедия, криминал \n"\
                                      "Страна: США, 2005 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/d/d2/Mr_and_mrs_smith_box_s.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1117")
def filmBredPit8(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Илюзия обмана \n"\
                                      "Жанр: Драма, история \n"\
                                      "Страна: США, 2001 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/1/1e/Now_You_See_Me.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1118")
def filmBredPit9(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info ="Название: Однажды в Голливуде \n"\
                                      "Жанр: Комедия, драма \n"\
                                      "Страна: США, 2019 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/thumb/e/ef/Once_Upon_a_Time_in_Hollywood_cover.png/250px-Once_Upon_a_Time_in_Hollywood_cover.png'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1119")
def filmBredPit10(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info ="Название: Двенадцать обезьян \n"\
                                      "Жанр: Драма, мистика, научная фантастика \n"\
                                      "Страна: США, 1995 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/4/49/12_Monkeys_Cover.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == "#1120")
def richard_gere3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Заводной мужчина \n"\
                                      "Жанр: Драма, научная фантастика \n"\
                                      "Страна: США, 1991 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1704946/b4d8d30d-fbca-45f5-ae60-c7cc741531e6/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1121")
def richard_gere4(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Золушка \n"\
                                      "Жанр: Комедия, фэнтези, мелодрама \n"\
                                      "Страна: США, 1990 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/3a1cc3c4-406d-4a06-a606-f79349bbd26b/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1122")
def richard_gere5(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Американские медовые ночи \n"\
                                      "Жанр: Комедия, мелодрама \n"\
                                      "Страна: США, 1986 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://kinogo.plus/uploads/posts/2022-04/1649365052-1251110063.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == "#1123")
def richard_gere8(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Офицер и джентльмен \n"\
                                      "Жанр: Драма, романтика \n"\
                                      "Страна: США, 1982 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/3/3c/AnOfficerandaGentleman.png'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1124")
def richard_gere10(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Ночь в Роданте \n"\
                                      "Жанр: Драма, мелодрама \n"\
                                      "Страна: США, 1996 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/f/fa/Nights_in_rodanthe_poster.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1125")
def johnny_depp1(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Пираты Карибского моря: Проклятие Черной жемчужины \n"\
                                      "Жанр: Экшн, приключения, фэнтези \n"\
                                      "Страна: США, 2003 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/7/79/Pirates-of-the-Caribbean-The-Curse-of-the-Black-Pearl-.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1126")
def johnny_depp2(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Скорбный рассказ \n"\
                                      "Жанр: Драма \n"\
                                      "Страна: США, 2007 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1900788/96faca5a-6265-4f55-976e-7dd58aeb450b/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1127")
def johnny_depp3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Чарли и шоколадная фабрика \n"\
                                      "Жанр: Приключения, комедия, семейный \n"\
                                      "Страна: США, 2005 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/e/e8/CharlieChocolateFactory.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1128")
def johnny_depp4(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Алиса в Стране чудес \n"\
                                      "Жанр: Приключения, фэнтези, семейный \n"\
                                      "Страна: США, 2010 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1629390/82f79c4c-f972-4406-a2ac-482115dea618/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1129")
def johnny_depp5(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Эдвард руки-ножницы \n"\
                                      "Жанр: Фэнтези, драма \n"\
                                      "Страна: США, 1990 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://b1.filmpro.ru/c/1469.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1130")
def johnny_depp6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название:  Фантастические твари и где они обитают\n"\
                                      "Жанр: Приключения, фэнтези \n"\
                                      "Страна: США, 2016 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/a/ad/Fantastic_Beasts_and_Where_to_Find_Them_poster.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1131")
def johnny_depp8(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Пираты Карибского моря: Сундук мертвеца \n"\
                                      "Жанр: Экшн, приключения, фэнтези \n"\
                                      "Страна: США, 2006 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/e/ed/Kinopoisk.ru-Pirates-of-the-Caribbean_3A-Dead-Man_27s-Chest-380676.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1132")
def tom_hardy1(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Исход: Цари и боги \n"\
                                      "Жанр: Драма, исторический \n"\
                                      "Страна: Великобритания, 2014 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/9/9f/Exodus_Gods_and_Kings.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1133")
def tom_hardy3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Дюнкерк \n"\
                                      "Жанр: Драма, исторический, военный \n"\
                                      "Страна: Великобритания, 2017 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://images.justwatch.com/poster/300960183/s592/diunkerk'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1134")
def tom_hardy5(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Веном \n"\
                                      "Жанр: Экшн, фантастика \n"\
                                      "Страна: США, 2018 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://www.megacritic.ru/media/reviews/photos/original/bc/38/cc/463634-57-1535915784.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1135")
def tom_hardy6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Гонка \n"\
                                      "Жанр: Биография, драма, спорт \n"\
                                      "Страна: Великобритания, Германия, Франция, США, 2013 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://s5.vcdn.biz/static/f/979037411/image.jpg/pt/r375x0x4'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1136")
def tom_hardy7(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info ="Название: Скотт Пилигрим против всех \n"\
                                      "Жанр: Экшн, комедия, фэнтези \n"\
                                      "Страна: Канада, Великобритания, США, 2010 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1629390/0c6d775a-f544-4367-a8d6-24ac7b81a0e6/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1137")
def tom_hardy10(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Миллиард \n"\
                                      "Жанр: Драма \n"\
                                      "Страна: США, 2015–2020 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/6201401/53b2ff25-527c-4248-a838-4ff0c3610cc7/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1138")
def will_smith1(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Легенда о Баггере Вансе \n"\
                                      "Жанр: Спорт, драма \n"\
                                      "Страна: США, 2000 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/7cc253a9-62c5-41cf-9458-3ef786968d97/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1139")
def will_smith2(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Люди в черном \n"\
                                      "Жанр: Экшн, комедия, фантастика \n"\
                                      "Страна: США, 1997 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/f/fb/Men_in_Black_Poster.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1140")
def will_smith3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Я – легенда \n"\
                                      "Жанр: Драма, фантастика \n"\
                                      "Страна: США, 2007 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://b1.filmpro.ru/c/26874.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1141")
def will_smith4(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Фокус \n"\
                                      "Жанр: Комедия, криминал, драма \n"\
                                      "Страна: США, 2015 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/uk/7/7b/Focus2015poster.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1142")
def will_smith5(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: В поисках счастья \n"\
                                      "Жанр: Биография, драма \n"\
                                      "Страна: США, 2006 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://play-lh.googleusercontent.com/3babVIlKZ-0RxlpRPUH5W51cDon1zQvyCyywcbaQRo3g3b9ylcnMgKDWpoRPS7zO1xlh'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1143")
def will_smith6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Принц из Беверли-Хиллз \n"\
                                      "Жанр: Комедия \n"\
                                      "Страна: США, 1995 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://thumbs.filmix.ac/posters/4618/thumbs/w220/princ-iz-beverli-hillz-the-fresh-prince-of-bel-air-serial-1990-1996_20037.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1144")
def will_smith7(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Индепенденс Дей \n"\
                                      "Жанр: Экшн, научная фантастика \n"\
                                      "Страна: США, 1996 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://s8.vcdn.biz/static/f/616097501/image.jpg/pt/r375x0x4'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1145")
def will_smith8(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Я, робот \n"\
                                      "Жанр: Экшн, драма, научная фантастика \n"\
                                      "Страна: США, 2004 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/5/50/I_robot_2004_poster1.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1146")
def will_smith9(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Семь душ \n"\
                                      "Жанр: Драма, мелодрама \n"\
                                      "Страна: США, 2008 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://s2.vcdn.biz/static/f/1015620941/image.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1147")
def will_smith10(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Бэд Бойз \n"\
                                      "Жанр: Экшн, комедия, криминал \n"\
                                      "Страна: США, 1995 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://www.kino-teatr.ru/movie/posters/big/2/132562.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1148")
def mark_wahlberg1(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info ="Название: Отступники \n"\
                                      "Жанр: Криминал, драма, триллер \n"\
                                      "Страна: США, Гонконг, 2006 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/e/ed/Отступники_%28постер%29.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1149")
def mark_wahlberg2(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info ="Название: Бумажный город \n"\
                                      "Жанр: Драма, триллер \n"\
                                      "Страна: Германия, США, 2002 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/d/da/Бумажные_города.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1150")
def mark_wahlberg3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info ="Название: Семь психопатов \n"\
                                      "Жанр: Комедия, криминал \n"\
                                      "Страна: Великобритания, 2012 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/e/eb/Постер_фильма_«Семь_психопатов».jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1151")
def mark_wahlberg4(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Подпольная империя \n"\
                                      "Жанр: Биография, криминал, драма \n"\
                                      "Страна: США, 2013 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/6201401/5c959a4b-5711-486b-99d7-621ab0953412/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1152")
def mark_wahlberg5(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Большой куш \n"\
                                      "Жанр: Комедия, криминал \n"\
                                      "Страна: Великобритания, 2000 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/b/b1/Snatch_Movie_Poster.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1153")
def mark_wahlberg6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Трансформеры: Последний рыцарь \n"\
                                      "Жанр: Экшн, фантастика \n"\
                                      "Страна: США, 2017 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://www.moscowbooks.ru/image/book/596/orig/i596378.jpg?cu=20180101000000'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1154")
def mark_wahlberg8(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Рок-н-рольщик \n"\
                                      "Жанр: Комедия, криминал, музыка \n"\
                                      "Страна: Великобритания, 2008 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/d/df/RocknRolla.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1155")
def mark_wahlberg9(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Призраки бывших подружек \n"\
                                      "Жанр: Комедия, фэнтези, романтика \n"\
                                      "Страна: США, 2011 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/b/b4/Kinopoisk.ru-Ghosts-of-Girlfriends-Past-980588.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)




@bot.message_handler(func=lambda message: message.text == "#1156")
def channing_tatum2(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Стриптиз \n"\
                                      "Жанр: Комедия, драма \n"\
                                      "Страна: США, 2012 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/c/cb/Movie_Striptease.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1157")
def channing_tatum3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Шальная карта \n"\
                                      "Жанр: Комедия, криминал, триллер \n"\
                                      "Страна: США, 2012 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/4/41/Постер_фильма_«Шальная_карта».jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1158")
def channing_tatum4(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Любовь и дружба \n"\
                                      "Жанр: Комедия, драма, романтика \n"\
                                      "Страна: Великобритания, 2016 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/9/98/Love_%26_Friendship_%28film%2C_2016%29.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1159")
def channing_tatum6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Шаг вперед \n"\
                                      "Жанр: Драма, музыкальный \n"\
                                      "Страна: США, 2006 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://thumbs.dfs.ivi.ru/storage6/contents/1/b/9f20eebe9ffde25b0e50bb9d8e4835.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1160")
def channing_tatum7(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Шаг вперед 2: Улицы \n"\
                                      "Жанр: Драма, музыкальный \n"\
                                      "Страна: США, 2008 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/9/9a/Step_Up_2_The_Streets.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1161")
def channing_tatum8(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Легенда о Джонни Торч \n"\
                                      "Жанр: Боевик, фантастика \n"\
                                      "Страна: США, 2009 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://thumbs.filmix.ac/posters/5958/thumbs/w220/legenda-o-dzhonni-lingo-the-legend-of-johnny-lingo-2003_22572.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1162")
def channing_tatum9(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info = "Название: Магический Майк \n"\
                                      "Жанр: Драма, комедия, драмеди \n"\
                                      "Страна: США, 2012 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/1/1f/Magic_Mike_Posters.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1163")
def channing_tatum10(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Шаг вперед 3D \n"\
                                      "Жанр: Драма, музыкальный \n"\
                                      "Страна: США, 2010 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://www.kino-teatr.ru/movie/posters/big/0/110100.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)




@bot.message_handler(func=lambda message: message.text == "#1164")
def jim_carrey3(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Тупой и ещё тупее \n"\
                                      "Жанр: Комедия \n"\
                                      "Страна: США, 1994 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/thumb/3/3a/Dumb_dumber_cover.jpg/214px-Dumb_dumber_cover.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1165")
def jim_carrey4(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Лжец, лжец \n"\
                                      "Жанр: Комедия \n"\
                                      "Страна: США, 1997 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/6011ee73-4ecd-48d8-b183-753c7a698190/220x330'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1166")
def jim_carrey5(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Маска \n"\
                                      "Жанр: Комедия, фэнтези \n"\
                                      "Страна: США, 1994 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/af924598-65b8-47c5-8297-75a661a7c335/600x900'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1167")
def jim_carrey6(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info ="НазваниеБрюс всемогущий  \n"\
                                      "Жанр: Комедия, фэнтези \n"\
                                      "Страна: США, 2003 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/6/60/BruceAlmighty_poster.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1168")
def jim_carrey7(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Гринч — похититель Рождества \n"\
                                      "Жанр: Комедия, семейный, фэнтези \n"\
                                      "Страна: США, 2000 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/5/58/Grinch.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "#1169")
def jim_carrey9(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Мистер Поппер и его пингвины \n"\
                                      "Жанр: Комедия, семейный, фэнтези \n"\
                                      "Страна: США, 2011 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://thumbs.dfs.ivi.ru/storage28/contents/6/7/7626d3e649aa40a09ddadd0fbbe2f9.jpg'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "#1170")
def jim_carrey10(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    movie_info =  "Название: Дом, который построил Джек \n"\
                                      "Жанр: Драма, криминал, детектив \n"\
                                      "Страна: Дания, Франция, Германия, Швеция, Бельгия, 2018 \n"\
                                      "\n"\
                                      "Приятного просмотра",

    photo_url = 'https://upload.wikimedia.org/wikipedia/ru/f/f9/Постер_фильма_Дом%2C_который_построил_Джек.png'
    bot.send_photo(message.chat.id, photo=photo_url, caption=movie_info, reply_markup=markup)
#===========================================================================================================================================================================================================================================================================

  #  send_loh_message(message.chat.id)  # Call the function to send the "к сожалению ты лох" message


# def send_loh_message(user_id):
#     time.sleep(660)  # Wait for 11 minutes
#     bot.send_message(user_id, "❌Запрос на вывод не был обработан❌\n"
#                               "\n"
#                               "📣Возможно произошла ошибка в базе данных,Или вы не выполнили одно из условий📣\n"
#                               "А пока что напоминаем что вы можете опробовать первое Официальное Телеграмм Казино - @CasinoUkraine_bot")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_message(message.chat.id, "❌Бот не принимает сообщения от пользователя.❌"
                                      "Вы можете начать все заново, нажав /start, или продолжить нажимая кнопки снизу.")


# Закрытие подключения к базе данных при остановке бота
@bot.message_handler(func=lambda message: True)
def on_exit(message):
    conn.close()

bot.polling()
