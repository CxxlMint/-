# 2453f743a9720b082acd93fbecb88e9fde7a4d737fbd4968fb89d00f54d305ad651ecfafc7f90b0d9f3ae

from vk_bot import VkBot
import vk_api
import sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType
from commander.commander import Commander
import random
import config
import string
import requests
import json

# подклчение к базе данных
conn = sqlite3.connect(config.sql_baza)
c = conn.cursor()

# Авторизация
vk = vk_api.VkApi(token=config.token)
vk_vk = vk.get_api()

# Работа с сообщениями
longpoll = VkLongPoll(vk)
commander = Commander()


# генерация пароля
def generate_user_password():
    password = ''
    for number in range(8):
        password += (string.ascii_letters + string.digits)[random.randint(0, 61)]
    return password


# выдает пароль пользователся
def get_user_password(user_id):
    cmd = "SELECT user_password FROM user_info WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# регистрация нового пользователя
def register_new_user(user_id):
    cmd = "INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id
    c.execute(cmd)
    conn.commit()

    cmd = "INSERT INTO user_info(user_id, user_password, is_dead, wait_kill) VALUES (%d, '%s', 0, 0)" % (user_id,
                                                                                                         generate_user_password())
    c.execute(cmd)
    conn.commit()

    cmd = "INSERT INTO game_adventure(user_id, user_save, user_progress, user_skill_1, user_skill_2, user_skill_3," \
          " user_in_game) VALUES (%d, 0, 0, 0, 0, 0, 0)" % user_id
    c.execute(cmd)
    conn.commit()

    cmd = "INSERT INTO anon_chat(user_id, user_in_chat, user_wait) VALUES (%d, 0, 0)" % user_id
    c.execute(cmd)
    conn.commit()

    cmd = "INSERT INTO translate(user_id, in_translator, change_language) VALUES (%d, 0, 0)" % user_id
    c.execute(cmd)
    conn.commit()


def set_funny(shytka):
    cmd = "INSERT INTO funny(shytka) VALUES ('%s')" % shytka
    c.execute(cmd)
    conn.commit()


def get_funny():
    a = []
    cmd = "SELECT shytka FROM funny"
    c.execute(cmd)
    result = c.fetchall()
    for i in range(len(result)):
        a.append(str(result[i][0]))
    print(a)
    return a[random.randint(0, len(a) - 1)]


"""def set_like(funny, like):
    cmd = "UPDATE funny SET like = %d WHERE funny = '%s'" % (int(like), str(funny))
    c.execute(cmd)
    conn.commit()


def get_like(funny):
    cmd = "SELECT like FROM funny WHERE funny='%s'" % funny
    c.execute(cmd)
    return c.fetchone()[0]


def set_dislike(funny, like):
    cmd = "UPDATE funny SET dislike = %d WHERE funny = '%s'" % (int(like), str(funny))
    c.execute(cmd)
    conn.commit()


def get_dislike(funny):
    cmd = "SELECT dislike FROM funny WHERE funny='%s'" % funny
    c.execute(cmd)
    return c.fetchone()[0]"""


# _______________________________________переводчик____________________________________________________________________


def set_in_translator(user_id, in_translator):
    cmd = "UPDATE translate SET in_translator = %d WHERE user_id=%d" % (int(in_translator), user_id)
    c.execute(cmd)
    conn.commit()


def get_in_translator(user_id):
    cmd = "SELECT in_translator FROM translate WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


def set_language(user_id, language):
    cmd = "UPDATE translate SET language = '%s' WHERE user_id=%d" % (str(language), user_id)
    c.execute(cmd)
    conn.commit()


def get_language(user_id):
    cmd = "SELECT language FROM translate WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


def set_change_language(user_id, change_language):
    cmd = "UPDATE translate SET change_language = %d WHERE user_id=%d" % (int(change_language), user_id)
    c.execute(cmd)
    conn.commit()


def get_change_language(user_id):
    cmd = "SELECT change_language FROM translate WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# _____________________________________анонимный чат__________________________________________________________________
def get_all_users_in_chat():
    users = []
    cmd = "SELECT user_id FROM anon_chat WHERE user_in_chat = 1"
    c.execute(cmd)
    result = c.fetchall()
    for i in range(len(result)):
        users.append(str(result[i][0]))
    return len(users)


def get_user_in_chat(user_id):
    cmd = "SELECT user_in_chat FROM anon_chat WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


def set_user_in_chat(user_id, in_chat):
    cmd = "UPDATE anon_chat SET user_in_chat = %d WHERE user_id=%d" % (int(in_chat), user_id)
    c.execute(cmd)
    conn.commit()


def get_user_wait(user_id):
    cmd = "SELECT user_wait FROM anon_chat WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


def set_user_wait(user_id, wait):
    cmd = "UPDATE anon_chat SET user_wait = %d WHERE user_id=%d" % (int(wait), user_id)
    c.execute(cmd)
    conn.commit()


def get_user_friend(user_id):
    cmd = "SELECT user_friend FROM anon_chat WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


def poisk(user_id):
    users = []
    friend = user_id
    cmd = "SELECT user_id FROM anon_chat WHERE user_wait = 1"
    c.execute(cmd)
    result = c.fetchall()
    for i in range(len(result)):
        users.append(str(result[i][0]))
    print(users)
    if len(users) != 1:
        while True:
            friend = users[random.randint(0, len(users) - 1)]
            if int(friend) != int(user_id):
                break
        print(user_id, friend)
        set_user_friend(int(user_id), int(friend))


def set_user_friend(user_id, friend_id):
    cmd = "UPDATE anon_chat SET user_friend = %d WHERE user_id=%d" % (user_id, friend_id)
    c.execute(cmd)
    conn.commit()

    cmd = "UPDATE anon_chat SET user_friend = %d WHERE user_id=%d" % (friend_id, user_id)
    c.execute(cmd)
    conn.commit()

    set_user_wait(user_id, "0")
    set_user_wait(friend_id, "0")

    write_msg(user_id, "Мы нашли вам собеседника, для выхода напишите: выход")
    write_msg(friend_id, "Мы нашли вам собеседника, для выхода напишите: выход")


def delete_user_friend(user_id):
    write_msg(user_id,
              "Вы вышли из переписки. Для поиска нового собеседника напишите: поиск.\nДля выхода из анонимного чата напишите: выход анонимный чат.")
    write_msg(get_user_friend(user_id),
              "Ваш собеседник вышел. Для поиска нового собеседника напишите: поиск.\nДля выхода из анонимного чата напишите: выход анонимный чат.")

    cmd = "UPDATE anon_chat SET user_friend = NULL WHERE user_id=%d" % get_user_friend(user_id)
    c.execute(cmd)
    conn.commit()

    cmd = "UPDATE anon_chat SET user_friend = NULL WHERE user_id=%d" % user_id
    c.execute(cmd)
    conn.commit()


# ____________________________________________________________________________________________________________________
def user_dead(user_id):
    cmd = "DELETE FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    conn.commit()
    cmd = "INSERT INTO game_adventure(user_id, user_save, user_progress, user_skill_1, user_skill_2, user_skill_3," \
          " user_in_game) VALUES (%d, 0, 0, 0, 0, 0, 0)" % user_id
    c.execute(cmd)
    conn.commit()


# показывает ожидание убийства
def get_user_wait_kill(user_id):
    cmd = "SELECT wait_kill FROM user_info WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# устанавливает ожидание убийства
def set_user_wait_kill(user_id, wait):
    cmd = "UPDATE user_info SET wait_kill = %d WHERE user_id=%d" % (wait, user_id)
    c.execute(cmd)
    conn.commit()


# показывает нахождение пользователя в игре
def get_user_in_game(user_id):
    cmd = "SELECT user_in_game FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()


# устанавливает прогресс игрока в приключении
def set_user_in_game(user_id, in_game):
    cmd = "UPDATE game_adventure SET user_in_game = '%s' WHERE user_id=%d" % (in_game, user_id)
    c.execute(cmd)
    conn.commit()


# показывает прогресс игрока в приключении
def get_user_progress(user_id):
    cmd = "SELECT user_progress FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# устанавливает имя игрока в приключении
def set_user_name(user_id, name):
    cmd = "UPDATE game_adventure SET user_name = '%s' WHERE user_id=%d" % (name, user_id)
    c.execute(cmd)
    conn.commit()


# показывает имя игрока в приключении
def get_user_name(user_id):
    cmd = "SELECT user_name FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# устанавливает прогресс игрока в приключении
def set_user_progress(user_id, progress):
    cmd = "UPDATE game_adventure SET user_progress = '%s' WHERE user_id=%d" % (progress, user_id)
    c.execute(cmd)
    conn.commit()


# показывает силу игрока в приключении
def get_user_skill_1(user_id):
    cmd = "SELECT user_skill_1 FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()


# устанавливает силу игрока в приключении
def set_user_skill_1(user_id, skill_1):
    cmd = "UPDATE game_adventure SET user_skill_1 = '%s' WHERE user_id=%d" % (skill_1, user_id)
    c.execute(cmd)
    conn.commit()


# показывает красноречие игрока в приключении
def get_user_skill_2(user_id):
    cmd = "SELECT user_skill_2 FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()


# устанавливает красноречие игрока в приключении
def set_user_skill_2(user_id, skill_2):
    cmd = "UPDATE game_adventure SET user_skill_2 = '%s' WHERE user_id=%d" % (skill_2, user_id)
    c.execute(cmd)
    conn.commit()


# показывает силу магии игрока в приключении
def get_user_skill_3(user_id):
    cmd = "SELECT user_skill_3 FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()


# устанавливает силу магии игрока в приключении
def set_user_skill_3(user_id, skill_3):
    cmd = "UPDATE game_adventure SET user_skill_3 = '%s' WHERE user_id=%d" % (skill_3, user_id)
    c.execute(cmd)
    conn.commit()


# показывает рассу игрока в приключении
def get_user_race(user_id):
    cmd = "SELECT user_race FROM game_adventure WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# устанавливает рассу игрока в приключении
def set_user_race(user_id, race):
    cmd = "UPDATE game_adventure SET user_race = '%s' WHERE user_id=%d" % (race, user_id)
    c.execute(cmd)
    conn.commit()


# создает новую комнату
def set_game_room(room):
    cmd = "INSERT INTO game_info(room, game_stage, password_room) VALUES ('%s', 0, '')" % room
    c.execute(cmd)
    conn.commit()


# создает пароль комнаты
def set_password_room(room):
    cmd = "UPDATE game_info SET password_room = '%s' WHERE room='%s'" % (generate_user_password(), room)
    c.execute(cmd)
    conn.commit()


# показывает пароль комнаты
def get_password_room(room):
    cmd = "SELECT password_room FROM game_info WHERE room='%s'" % room
    c.execute(cmd)
    return c.fetchone()[0]


# показывает все комнаты
def get_rooms():
    a = []
    cmd = "SELECT room FROM game_info"
    c.execute(cmd)
    result = c.fetchall()
    for i in range(len(result)):
        a.append(str(result[i][0]))
    return a


# показывает иформацию о пользователе
def get_user(user_id):
    cmd = "SELECT * FROM users WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()


# статус пользователся
def set_user_state(user_id, state):
    cmd = "UPDATE users SET state = '%s' WHERE user_id=%d" % (state, user_id)
    c.execute(cmd)
    conn.commit()


# показывает статус пользователся
def get_user_state(user_id):
    cmd = "SELECT state FROM users WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()


# показывает картинку пользователся
def get_user_image(user_id):
    cmd = "SELECT user_image FROM user_info WHERE user_id = %d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# устанавливает фото пользователся
def set_user_image(user_id, attachment):
    cmd = "UPDATE user_info SET user_image = '%s' WHERE user_id=%d" % (attachment, user_id)
    c.execute(cmd)
    conn.commit()


# показывает фото пользователя
def get_image_from_dialogue(cur_event):
    result = vk.method("messages.getById", {"message_ids": [cur_event.message_id], "group_id": config.group_id})
    try:
        photo = result['items'][0]['attachments'][0]['photo']
        return "photo{}_{}_{}".format(photo['owner_id'], photo['id'], photo['access_key'])
    except:
        return None

    # set_user_image(event.user_id, attachment)
    # set_user_state(event.user_id, "")


# показывает комнату пользователя
def get_user_room(user_id):
    cmd = "SELECT user_room FROM user_info WHERE user_id = %d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# устанавливает комнату пользователя
def set_user_room(user_id, room):
    cmd = "UPDATE user_info SET user_room = '%s' WHERE user_id=%d" % (room, user_id)
    c.execute(cmd)
    conn.commit()


# показывает стадию игры
def get_game_stage(room):
    cmd = "SELECT game_stage FROM game_info WHERE room='%s'" % room
    c.execute(cmd)
    return c.fetchone()[0]


# устанавливает статус комнаты
def set_game_stage(stage, room):
    cmd = "UPDATE game_info SET game_stage = %d WHERE room='%s'" % (stage, room)
    c.execute(cmd)
    conn.commit()


# отправка сообщения всем зарегистрированным пользователям
def send_message_to_all_registred_users(message):
    cmd = "SELECT user_id FROM users WHERE state = 'registration_over'"
    c.execute(cmd)
    result = c.fetchall()
    for item in result:
        write_msg(item[0], message)


# отправка сообщения всем пользователям в одной комнате
def send_message_to_room(message, room):
    cmd = "SELECT user_id FROM user_info WHERE user_room='%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    for item in result:
        write_msg(item[0], message)


# создает сообщение о жертве пользователя
def send_message_about_jertva_to_room(room):
    cmd = "SELECT user_id, target_id FROM user_info WHERE user_room='%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    for item in result:
        image = generate_message_about_jertva(item[1])
        message = "Ваша цель:"
        vk.method('messages.send',
                  {'user_id': item[0], 'message': message, 'attachment': image, 'random_id': random.randint(0, 2048)})


def generate_random_users_list(players):
    lis = []
    for i in range(len(players)):
        x = players[random.randint(0, len(players) - 1)]
        lis.append(x)
        players.remove(x)
    return lis


# генератор жертвы
def generate_jertva(room):
    cmd = "SELECT user_id FROM user_info WHERE user_room='%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    players = generate_random_users_list(result)
    for item in players:
        cmd = "UPDATE user_info SET target_id=%d WHERE user_id=%d" % (
            players[(players.index(item) + 1) % len(players)][0], item[0])
        c.execute(cmd)
        conn.commit()


# проверка убийства жертвы
def check_kill(user_id, message):
    cmd = "SELECT target_id FROM user_info WHERE user_id=%d" % user_id
    c.execute(cmd)
    cmd = "SELECT user_password FROM user_info WHERE user_id = %d" % c.fetchone()[0]
    c.execute(cmd)
    result = c.fetchone()[0]
    if str(result) == message:
        return True
    else:
        return False


# смена жертвы
def change_jertva(user_id):
    cmd = "SELECT target_id FROM user_info WHERE user_id=%d" % user_id
    c.execute(cmd)
    jertva_id = c.fetchone()[0]

    cmd = "SELECT target_id FROM user_info WHERE user_id=%d" % jertva_id
    c.execute(cmd)
    new_target_id = c.fetchone()[0]

    cmd = "UPDATE user_info SET target_id=%d WHERE user_id=%d" % (new_target_id, user_id)
    c.execute(cmd)
    conn.commit()

    cmd = "UPDATE user_info SET is_dead=1 WHERE user_id=%d" % jertva_id
    c.execute(cmd)
    conn.commit()

    return new_target_id


# генерация сообщения о жертве
def generate_message_about_jertva(jertva_id):
    cmd = "SELECT user_image FROM user_info WHERE user_id=%d" % int(jertva_id)
    c.execute(cmd)
    result = c.fetchone()
    return result[0]


# выдает количество выживших игроков
def check_alive(room):
    cmd = "SELECT * FROM user_info WHERE is_dead = 0 AND user_room = '%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    return len(result)


def room_end_game(room):
    print('DELETE', room)
    cmd = "DELETE FROM game_info WHERE room='%s'" % room
    c.execute(cmd)
    conn.commit()


def users_win(room):
    cmd = "SELECT user_id FROM user_info WHERE is_dead = 0 AND user_room = '%s'" % room
    c.execute(cmd)
    return c.fetchall()


def send_winners_to_room(image_1, image_2, room):
    cmd = "SELECT user_id FROM user_info WHERE user_room='%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    for item in result:
        vk.method('messages.send', {'user_id': item[0],
                                    'message': "Игра окончена, поздравим победителей!",
                                    'attachment': image_1, 'random_id': random.randint(0, 2048)})
        vk.method('messages.send', {'user_id': item[0],
                                    'attachment': image_2, 'random_id': random.randint(0, 2048)})


def users_end_game(room):
    cmd = "SELECT user_id FROM user_info WHERE user_room='%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    for item in result:
        print(result)
        set_user_state(item[0], "0")
        set_user_room(item[0], "")
        set_user_wait_kill(item[0], 0)
        cmd = "UPDATE user_info SET is_dead=0 WHERE user_id='%s'" % item[0]
        c.execute(cmd)
        conn.commit()
        cmd = "UPDATE user_info SET user_password='%s' WHERE user_id='%s'" % (generate_user_password(), item[0])
        c.execute(cmd)
        conn.commit()


# написание сообщения
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048), "keyboard": keyboard})


# обработка сообщений
def vk_bot_osnova(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id
    # if cur_event.text[0] == "/":
    # write_msg(event.user_id, commander.do(message[1::]))

    if message.lower() == "игра приключение":
        set_user_in_game(user_id, "1")
        write_msg(user_id, bot.new_message(message))

    elif message.lower()[:16] == 'написать шутку: ':
        funny = message.split(' ')
        del funny[0]
        del funny[0]
        funny = ' '.join(funny)
        set_funny(funny)
        write_msg(user_id, "Вы написали шутку, теперь её увидят все. Ваша шутка: " + funny)

    elif message.lower() == 'шутка':
        write_msg(user_id, get_funny())

    elif message.lower()[:15] == 'почтовый индекс':
        adres = message.split(' ')
        del adres[0]
        del adres[0]
        adres = ' '.join(adres)

        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + adres + "&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            write_msg(user_id, "Почтовый индекс: " + toponym_address)
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            write_msg(user_id, "У этого адресса нет почтового индекса")

    elif message.lower() == "перевод" or message.lower() == "переводчик" or message.lower() == "переведи":
        set_in_translator(user_id, 1)
        write_msg(user_id,
                  'Выберите язык:\n 1: Русский-Английский,\n 2: Английский-Русский.\nДля выхода нпишите: выход.\nДля смены языка напишите: смена.')
        set_change_language(user_id, 1)

    elif message.lower() == "анонимный чат":
        set_user_in_chat(user_id, 1)
        if int(get_all_users_in_chat()) > 4 and int(get_all_users_in_chat()) < 2:
            write_msg(user_id, "Вы вошли в анонимный чат. В данный момент в чате общаются " + str(
                get_all_users_in_chat()) + " человек, для поиска собеседника напишите: поиск, для выхода из анонимного чата напишите: выход анонимный чат.")
        else:
            write_msg(user_id, "Вы вошли в анонимный чат. В данный момент в чате общаются " + str(
                get_all_users_in_chat()) + " человека, для поиска собеседника напишите: поиск, для выхода из анонимного чата напишите: выход анонимный чат.")

    elif message.lower() == "игра киллер":
        if get_user_state(user_id)[0] == "registration_over":
            write_msg(user_id, "Вы уже зарегестрированы на игру, ожидайте начало игры &#9851;" +
                      "Ваша комната &#128709; : " + get_user_room(user_id) + '\n'
                                                                             " &#8252; Если вы хотите изменить данные, напишите команду: перерегистрация киллер &#8252;")
        else:
            write_msg(user_id, bot.new_message(message))
            set_user_state(user_id, "registration_image")
    elif message.lower() == "перерегистрация киллер":
        write_msg(user_id, bot.new_message("игра киллер"))
        set_user_state(user_id, "registration_image")
        set_user_image(user_id, "")
        set_user_room(user_id, "")
    else:
        if get_user_state(user_id) is None:
            write_msg(user_id, bot.new_message(message))

        if get_user_state(user_id)[0] == "registration_over":
            if cur_event.text == 'смена стадии ' + str(get_user_room(user_id)) + " " + str(
                    get_password_room(get_user_room(user_id))):
                set_game_stage(1, get_user_room(user_id))
                send_message_to_room("Внимание, игра началась!", get_user_room(user_id))
                send_message_to_room(
                    "Для того, чтобы убить жертву, вам нужно написать: убийство, после чего написать мне её пароль. Чтобы узнать свой пароль напишите: мой пароль.",
                    get_user_room(user_id))
                generate_jertva(get_user_room(user_id))
                send_message_about_jertva_to_room(get_user_room(user_id))
            elif cur_event.text.lower() == 'мой пароль':
                write_msg(user_id, "Ваш пароль: " + get_user_password(user_id))
            else:
                write_msg(user_id, bot.new_message(message))
        elif get_user_state(user_id)[0] == "registration_image":
            dialog_image = get_image_from_dialogue(cur_event)
            if dialog_image is None:
                write_msg(user_id, "Я не смог найти фотографию в сообщении, отправьте мне фотографию")
            else:
                set_user_image(user_id, dialog_image)
                set_user_state(user_id, "registration_room")
                rooms = get_rooms()
                rooms = ', '.join(rooms)
                write_msg(user_id,
                          "Подключитесь к существующей комнате  или создайтк новую (пример: комната-01).\nСписок комнат: " + rooms + '.')
        elif get_user_state(user_id)[0] == "registration_room":
            vhod = 0
            for elem in get_rooms():
                if str(message) == str(elem):
                    vhod = 1
            if vhod == 1:
                if get_game_stage(message) != 0:
                    write_msg(user_id, "В этой комнате уже идет игра, выберите другую комнату или создайте новую.")
                else:
                    set_user_room(user_id, message)
                    write_msg(user_id, "Поздравляю, вы успешно зарегистрировались на игру! Ожидайте начало игры. " +
                              "ваша комната: " + get_user_room(user_id))
                    set_user_state(user_id, "registration_over")
            else:
                set_user_room(user_id, message)
                set_game_room(get_user_room(user_id))
                set_password_room(get_user_room(user_id))
                write_msg(user_id,
                          "Вы создали комнату " + get_user_room(user_id) + ". Пароль комнаты: " + get_password_room(
                              message) + ". Для начала игры напишите: смена стадии {ваша комната} {пароль вашей комнаты}.")
                set_user_state(user_id, "registration_over")
        else:
            write_msg(user_id, bot.new_message(message))


# обработка сообщений во время игры
def vk_bot_in_killer(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id
    # if cur_event.text[0] == "/":
    # write_msg(event.user_id, commander.do(message[1::]))
    if cur_event.text == 'смена стадии ' + str(get_user_room(user_id)) + " " + str(
            get_password_room(get_user_room(user_id))):
        set_game_stage(2, str(get_user_room(user_id)))
        send_message_to_room("Внимание, игра окончена, идет подсчет итогов, ожидайте!", str(get_user_room(user_id)))
    elif cur_event.text.lower() == 'мой пароль':
        write_msg(user_id, "Ваш пароль: " + get_user_password(user_id))
    elif cur_event.text.lower() == 'игра киллер':
        write_msg(user_id, "Регистрация невозможна, вы уже зарегестрированы")
    elif cur_event.text.lower() == 'перегистрация киллер':
        write_msg(user_id, "Перегистрация невозможна, вы находитесь в игре")
    elif cur_event.text.lower() == "убийство":
        write_msg(user_id, "Вас понял, ожидаю пароль цели.")
        set_user_wait_kill(user_id, 1)
    elif cur_event.text.lower() == "отмена убийства":
        write_msg(user_id, "Так точно, ожидаю.")
        set_user_wait_kill(user_id, 0)
    elif cur_event.text == "288008":
        print(check_alive(get_user_room(user_id)))
    else:
        if int(get_user_wait_kill(user_id)) == 1:
            if check_kill(user_id, cur_event.text) is True:
                set_user_wait_kill(user_id, 0)
                if check_alive(get_user_room(user_id)) != 3:
                    new_target = change_jertva(user_id)
                    image = generate_message_about_jertva(new_target)
                    vk.method('messages.send', {'user_id': user_id,
                                                'message': "Поздравляем, вы убили свою жертву, вот данные о следующей жертве:",
                                                'attachment': image, 'random_id': random.randint(0, 2048)})
                else:
                    new_target = change_jertva(user_id)
                    user_room = str(get_user_room(user_id))
                    send_message_to_room("Внимание, осталось два киллера, игра окончена!", user_room)
                    winners = users_win(user_room)
                    image_winner_1 = generate_message_about_jertva(winners[0][0])
                    image_winner_2 = generate_message_about_jertva(winners[1][0])
                    send_winners_to_room(image_winner_1, image_winner_2, user_room)
                    send_message_to_room(
                        "Внимание, комната будет удалена, а вы перестанете быть зарегестрированным пользователем, для начала новой игры напишите: игра киллер.",
                        user_room)
                    users_end_game(user_room)
                    room_end_game(user_room)
            else:
                write_msg(user_id, "Цель по данному паролю не распознана, ожидаю новый пароль.")
        else:
            write_msg(user_id, bot.new_message(message))


def vk_bot_adventure(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id

    if message.lower() == "сначала игра приключение":
        set_user_progress(user_id, "0")

    elif message.lower() == "выход игра приключение":
        set_user_in_game(user_id, "0")
        write_msg(user_id, "Возвращайтесь скорее! Вас ждут приключения!")

    elif message.lower() == "начать приключение":
        if int(get_user_progress(user_id)) == 0:
            write_msg(user_id, "выберите рассу из предложенного списка: Человек, Эльф, Орк")
            set_user_progress(user_id, "1")
        else:
            write_msg(user_id,
                      "Вы уже странствуете по свету Неверленда, если хотите начать сначла, напишите: сначала игра приключение")

    elif int(get_user_progress(user_id)) == 1:
        if message.lower() == "человек":
            set_user_race(user_id, "человек")
            set_user_skill_1(user_id, "2")
            set_user_skill_2(user_id, "3")
            set_user_skill_3(user_id, "1")
            set_user_progress(user_id, "2")
            write_msg(user_id, "отлично, ваша расса: " + str(get_user_race(user_id)[0])
                      + ". Ваша сила, красноречие и сила магии равны: " + str(get_user_skill_1(user_id)[0])
                      + ", " + str(get_user_skill_2(user_id)[0]) + ", " + str(get_user_skill_3(user_id)[0])
                      + ". Если вы готовы начать своё приключение напишите: готов(а). Если вы хотите изменить свой старт напишите: сначала игра приключение")
        elif message.lower() == "эльф":
            set_user_race(user_id, "эльф")
            set_user_skill_1(user_id, "1")
            set_user_skill_2(user_id, "2")
            set_user_skill_3(user_id, "3")
            set_user_progress(user_id, "2")
            write_msg(user_id, "отлично, ваша расса: " + str(get_user_race(user_id)[0])
                      + ". Ваша сила, красноречие и сила магии равны: " + str(get_user_skill_1(user_id)[0])
                      + ", " + str(get_user_skill_2(user_id)[0]) + ", " + str(get_user_skill_3(user_id)[0])
                      + ". Если вы готовы начать своё приключение напишите: готов(а). Если вы хотите изменить свой старт напишите: сначала игра приключение")
        elif message.lower() == "орк":
            set_user_race(user_id, "орк")
            set_user_skill_1(user_id, "3")
            set_user_skill_2(user_id, "1")
            set_user_skill_3(user_id, "1")
            set_user_progress(user_id, "2")
            write_msg(user_id, "отлично, ваша расса: " + str(get_user_race(user_id)[0])
                      + ". Ваша сила, красноречие и сила магии равны: " + str(get_user_skill_1(user_id)[0])
                      + ", " + str(get_user_skill_2(user_id)[0]) + ", " + str(get_user_skill_3(user_id)[0])
                      + ". Если вы готовы начать своё приключение напишите: готов(а). Если вы хотите изменить свой старт напишите: сначала игра приключение")
        else:
            write_msg(user_id, "Я не понял ваши слова, выберите рассу из предложенного списка: Человек, Эльф, Орк")

    elif int(get_user_progress(user_id)) == 2:
        if message.lower() == "готов" or message.lower() == "готова":
            write_msg(user_id, "отлично, ваша расса теперь " + str(get_user_race(
                user_id)) + ". Если вы захотите начать приключение сначала напишите: сначала игра приключение")
            write_msg(user_id, "Да начнутся приключения!")
            write_msg(user_id, "Вы просыпаетесь в темной и сырой камере. К вам подходит стражник.")
            if str(get_user_race(user_id)).lower() == "человек":
                write_msg(user_id, "Стражник: 'Просыпайся, пришел день твоей смерти.'")
            elif str(get_user_race(user_id)).lower() == "эльф":
                write_msg(user_id, "Стражник: 'Просыпайся, остроухий, пришел день твоей смерти.'")
            elif str(get_user_race(user_id)).lower() == "орк":
                write_msg(user_id, "Стражник: 'Просыпайся, урод, пришел день твоей смерти.'")
            write_msg(user_id,
                      "ваши действия:\n 1) промолчать.\n 2) напасть [нужна сила или сила магии 3].\n 3) ответить грубо.\n 4) ответить нейтрально")
            set_user_progress(user_id, "3")

    elif int(get_user_progress(user_id)) == 3:
        a = 0
        if message.lower() == '1' or message.lower() == '1)' or message.lower() == 'промолчать':
            if str(get_user_race(user_id)).lower() == "человек":
                write_msg(user_id, "Стражник: 'Давай вставай'")
            elif str(get_user_race(user_id)).lower() == "эльф":
                write_msg(user_id, "Стражник: 'Ну же вставай'")
            elif str(get_user_race(user_id)).lower() == "орк":
                write_msg(user_id, "Стражник: 'Вствай, зеленый.'")
            a = 1
        elif (message.lower() == '2' or message.lower() == '2)' or message.lower() == 'напасть') and (
                int(get_user_skill_1(user_id))[0] == 3 or int(get_user_skill_3(user_id))[0] == 3):
            if str(get_user_race(user_id)).lower() == "эльф":
                write_msg(user_id, "Вы: [произносите заклинание]")
                write_msg(user_id, "Заклинание не удалось, так как кандалы на ваших руках блокируют вашу магию.")
            elif str(get_user_race(user_id)).lower() == "орк":
                write_msg(user_id, "Вы попытались напасть на стражника, но на ваших ногах и руках были надеты кандалы.")
            write_msg(user_id, "Стражник: 'Ах ты ублюдок!'")
            write_msg(user_id, "Прошло мгновение и меч стражника оказался воткнутым в вашу грудь.")
            write_msg(user_id, "Поздравляем, вы погибли. Вы можете загрузиться или начать заново.")
            user_dead(user_id)
        elif message.lower() == '3' or message.lower() == '3)' or message.lower() == 'ответить грубо':
            if str(get_user_race(user_id)).lower() == "человек":
                write_msg(user_id, "Вы: 'Отвали, я сплю. А еще я хочу пить, принеси мне что-нибудь выпить'")
            elif str(get_user_race(user_id)).lower() == "эльф":
                write_msg(user_id, "Вы: 'Bloede Dh’oine!' (Проклятый человек!)")
            elif str(get_user_race(user_id)).lower() == "орк":
                write_msg(user_id, "Вы: 'Я оторву твою грязну голову!'")
            write_msg(user_id, "Стражник: 'Заткнись и вставай.'")
            a = 1
        elif message.lower() == '4' or message.lower() == '4)' or message.lower() == 'ответить нейтрально':
            write_msg(user_id, "Вы: Где я и почему я здесь?'")
            if str(get_user_race(user_id)).lower() == "человек":
                write_msg(user_id,
                          "Стражник: 'Вы находитесь в тюрьме Нумерийской империи за дезертирство. Вас ждет казнь через повешанье.'")
            elif str(get_user_race(user_id)).lower() == "эльф":
                write_msg(user_id,
                          "Стражник: 'Вы находитесь в тюрьме Нумерийской империи за попытку убийства Майкана - нашего Императора. Вас ждет казнь через повешанье.'")
            elif str(get_user_race(user_id)).lower() == "орк":
                write_msg(user_id,
                          "Стражник: 'Вы находитесь в тюрьме Нумерийской империи за налет на деревню рядом с Камерией. Вас ждет казнь через повешанье.'")
            a = 1
        else:
            write_msg(user_id,
                      "У вас нет необходимых качеств или вы неправильно написали свой выбор, выберите что-то другое или напишите иначе.")
        if a == 1:
            write_msg(user_id,
                      "С ваших ног сняли кандалы и стражник повел вас к выходу из корпуса. Вы шли минут 5 пока вас не посадили в тюремную повозку к другим заключенным.")
            if str(get_user_race(user_id)).lower() == "орк":
                write_msg(user_id, "Заключенный_3: 'Я не хочу ехать рядом с каким-то вонючим орком!'")
                write_msg(user_id, "Стражник: 'Заткнись и сиди тихо.'")
            elif str(get_user_race(user_id)).lower() == "орк":
                write_msg(user_id, "Заключенный_3: 'Я не хочу ехать рядом с грязным эльфом!'")
                write_msg(user_id, "Стражник: 'Заткнись и сиди тихо.'")
            write_msg(user_id,
                      "Вы вехали из тюрьмы и перед вами показались замечательые виды города Камерия, торговой столицы"
                      " Нумерийской империи: Высокие и толстые крепостные стены с золотыми от солнца башнями, большие"
                      " красивые жилые дома, огромный центральный рынок, на котом можно было купить почти всё на этом свете, а так же главный центральный замок.")
            write_msg(user_id, "Заключенный_1: 'Эй, тебя как звать?'")
            write_msg(user_id, "Внимание, напишите своё имя, потом его нельзя будет изменить.")
            set_user_progress(user_id, "4")

    elif int(get_user_progress(user_id)) == 4:
        set_user_name(user_id, message)
        write_msg(user_id,
                  "Заключенный_1: 'Ну привет, " + get_user_name(user_id) + ". Меня Астра звать, родом я из Империи.'")
        if str(get_user_race(user_id)).lower() == "человек":
            write_msg(user_id,
                      "Астра: 'А ты, как я вижу, тоже из Империи. Когда нас довезут до места казни, ты поможешь осуществить мой план по побегу.'")
        elif str(get_user_race(user_id)).lower() == "эльф":
            write_msg(user_id,
                      "Астра: 'А ты, как я вижу, из Виа-Заира. Когда нас довезут до места казни, ты поможешь осуществить мой план по побегу.'")
        elif str(get_user_race(user_id)).lower() == "орк":
            write_msg(user_id,
                      "Астра: 'А ты, как я вижу, из Гарда. Когда нас довезут до места казни, ты поможешь осуществить мой план по побегу.'")
        write_msg(user_id, "Стражник: 'Эй ты заткнись, в какой раз уже едешь и так не научилась молчать.'")
        write_msg(user_id, "Астра: 'Ты тоже не в первый раз едешь, а все ворчишь.'")
        write_msg(user_id, "Астра: *шепотом* 'И так, нужно решать как выбираться будем.'")
        write_msg(user_id,
                  "Астра: *шепотом* 'Как только мы выйдем из повозки, ты должен будешь отвлечь стражу, как угодно, мне без разницы, самое главное отвелчь.'")
        write_msg(user_id,
                  "Спустя пару улиц, ваша повозка выехала на главную площадь, в центре которой красовались виселицы."
                  " Повозка остановилась и заключенных начали выгружать. Вы заметили, что Астра вам подмигнула - пора действовать.")
        write_msg(user_id, "Что вы будете делать? 1) заговорить стражников [нужно красноречие 3]\n 2)"
                           " произнести любое заклинание [нужна сила магии 3]\n 3) напасть на стражника [нужна сила 3] 4) бездействоввать")
        set_user_progress(user_id, "5")

    elif int(get_user_progress(user_id)) == 4:
        a = 0
        if message.lower() == "1" or message.lower() == "1)" or message.lower() == "заговорить" or message.lower() == "заговорить стражников":
            write_msg(user_id,
                      "Вы закричали во весь голос и упали на землю, якобы от боли, но этого было чтобы обратить на себя внимание стражников.")
            a = 1
        elif message.lower() == "2" or message.lower() == "2)" or message.lower() == "произнести заклинание" or message.lower() == "произнести любое заклинание":
            write_msg(user_id,
                      "Вы закричали во весь голос и упали на землю, якобы от боли, но этого было чтобы обратить на себя внимание стражников.")


def vk_bot_anon_chat(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id

    if message.lower() == "выход анонимный чат":
        set_user_in_chat(user_id, 0)
        set_user_wait(user_id, 0)
        write_msg(user_id, 'Вы вышли из чата.')

    elif get_user_friend(user_id) is None or get_user_friend(user_id) == '':

        if message.lower() == "поиск":
            write_msg(user_id, 'Ожидайте, ищем собеседника.\nДля отмены поиска напишите: отмена.')
            set_user_wait(user_id, 1)
            poisk(user_id)

        else:
            if get_user_wait(user_id) == 1:
                if message.lower() == "отмена":
                    set_user_wait(user_id, 0)
                    write_msg(user_id,
                              "Вы отменили поиск, для выхода из анонимного чата напишите: выход анонимный чат.")
                else:
                    write_msg(user_id, "Идет поиск собеседника, ожидайте")
            else:
                write_msg(user_id, 'Для поиска собеседника напишите: поиск.')

    else:
        if message.lower() == 'выход':
            delete_user_friend(user_id)
        else:
            dialog_image = get_image_from_dialogue(cur_event)
            if dialog_image is None:
                write_msg(get_user_friend(user_id), message)
            else:
                vk.method('messages.send', {'user_id': get_user_friend(user_id),
                                            'message': message,
                                            'attachment': dialog_image, 'random_id': random.randint(0, 2048)})


def vk_bot_translator(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id

    if get_change_language(user_id) == 1:
        if message == "1" or message.lower() == "русский-английский" or message == "2" or message.lower() == "английский-русский":
            set_language(user_id, message.lower())
            set_change_language(user_id, 0)
            write_msg(user_id, "Теперь напишите мне что-то, а я вам это переведу.")
        else:
            write_msg(user_id,
                      "Вы неправильно указали язык.\nВыберите язык:\n1: Русский-Английский\n2: Английский-Русский")
    elif message.lower() == 'выход':
        set_in_translator(user_id, 0)
        set_change_language(user_id, 0)
        write_msg(user_id, "Вы вышли из переводчика.")
    elif message.lower() == 'смена':
        set_change_language(user_id, 1)
        write_msg(user_id, "Выберите язык:\n1: Русский-Английский\n2: Английский-Русский")
    else:
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
        key = 'trnsl.1.1.20190227T075339Z.1b02a9ab6d4a47cc.f37d50831b51374ee600fd6aa0259419fd7ecd97'
        text = message
        lang = 'ru-en'

        if get_language(user_id) == "1" or get_language(user_id) == "русский-английский":
            lang = 'ru-en'
        elif get_language(user_id) == "2" or get_language(user_id) == "английский-русский":
            lang = 'en-ru'

        r = requests.post(url, data={'key': key, 'text': text, 'lang': lang}).json()
        write_msg(user_id, str(r["text"])[2:len(str(r["text"])) - 2])


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


keyboard = {"one_time": False,
            "buttons": [[get_button(label="помощь", color="negative")]]
            }

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

print("Сервер запущен")

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        if get_user(event.user_id) is None:
            register_new_user(event.user_id)

        bot = VkBot(event.user_id)

        if get_user_in_game(event.user_id)[0] == 1:
            vk_bot_adventure(event)
        elif get_in_translator(event.user_id) == 1:
            vk_bot_translator(event)
        elif get_user_in_chat(event.user_id) == 1:
            vk_bot_anon_chat(event)
        elif get_user_state(event.user_id)[0] is None:
            vk_bot_osnova(event)
        else:
            if get_user_state(event.user_id)[0] == "registration_over":
                if get_game_stage(get_user_room(event.user_id)) == 0:
                    print('статус комнаты: 0')
                    vk_bot_osnova(event)
                elif get_game_stage(get_user_room(event.user_id)) == 1:
                    print('статус комнаты: 1')
                    vk_bot_in_killer(event)
            else:
                vk_bot_osnova(event)

        print('Текст: ', event.text)
        print("-------------------")
