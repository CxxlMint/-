# 2453f743a9720b082acd93fbecb88e9fde7a4d737fbd4968fb89d00f54d305ad651ecfafc7f90b0d9f3ae

from vk_bot import VkBot
import random
import vk_api
import sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType
from commander.commander import Commander
import random
import config
import string
# подклчение к базе данных
conn = sqlite3.connect(config.sql_baza)
c = conn.cursor()

# Авторизация
vk = vk_api.VkApi(token=config.token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)
commander = Commander()


# генерация пароля
def generate_user_password():
    password = ''
    for number in range(8):
        password += (string.ascii_letters + string.digits)[random.randint(0, 61)]
    return password


# регистрация нового пользователя
def register_new_user(user_id):
    cmd = "INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id
    c.execute(cmd)
    conn.commit()
    cmd = "INSERT INTO user_info(user_id, user_password, is_dead) VALUES (%d, '%s', 0)" % (user_id,
                                                                                           generate_user_password())
    c.execute(cmd)
    conn.commit()


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


def set_user_image(user_id, attachment):
    cmd = "UPDATE user_info SET user_image = '%s' WHERE user_id=%d" % (attachment, user_id)
    c.execute(cmd)
    conn.commit()


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
def get_game_stage():
    cmd = "SELECT game_stage FROM game_info"
    c.execute(cmd)
    return c.fetchone()[0]


def set_game_stage(stage):
    cmd = "UPDATE game_info SET game_stage = %d" % stage
    c.execute(cmd)
    conn.commit()


def send_message_to_all_users(message):
    cmd = "SELECT user_id FROM users WHERE state = 'registration_over'"
    c.execute(cmd)
    result = c.fetchone()
    for item in result:
        write_msg(item, message)


# написание сообщения
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


# обработка сообщений
def check_message(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id
    # if cur_event.text[0] == "/":
    # write_msg(event.user_id, commander.do(message[1::]))
    if get_user_state(user_id) is None:
        write_msg(user_id, bot.new_message(message))
    elif message.lower() == "регистрация киллер":
        if get_user_state(user_id)[0] == "registration_over":
            write_msg(user_id, "Вы уже зарегестрированы на игру, ожидайте начало игры &#9851;" +
                      "Ваша комната &#128709; : " + get_user_room(user_id) + '\n'
                      " &#8252; Если вы хотите изменить данные, напишите команду: перерегистрация киллер &#8252;")
        else:
            write_msg(user_id, bot.new_message(message))
            set_user_state(user_id, "registration_image")
    elif message.lower() == "перерегистрация киллер":
        write_msg(user_id, bot.new_message("регистрация киллер"))
        set_user_state(user_id, "registration_image")
        set_user_image(user_id, "")
        set_user_room(user_id, "")
    elif cur_event.text == 'сМенА СтаДИи ' + config.admin_password:
        cur_stage = get_game_stage()
        set_game_stage(int(cur_stage) + 1)
        if cur_stage == 1:
            send_message_to_all_users("Внимание, игра началась!")
        elif cur_stage == 2:
            send_message_to_all_users("Внимание, игра окончена, идет подсчет итогов, ожидайте!")
        else:
            send_message_to_all_users("Внимание, итог игры готов, победители: " + ".")
    else:
        # if get_user_state(user_id) == "registration":
        #    print(get_user_image(user_id), '12')
        #    if get_user_image(user_id) is None:
        #        set_user_state(user_id, "registration_image")
        #        if get_image_from_dialogue(cur_event) is None:
        #            write_msg(user_id, "Я не смог найти фотографию в сообщении, отправьте мне фотографию")
        #        else:
        #            write_msg(user_id, bot.new_message(message))
        #    else:
        #        write_msg(user_id, bot.new_message(message))
        if get_user_state(user_id)[0] == "registration_image":
            dialog_image = get_image_from_dialogue(cur_event)
            if dialog_image is None:
                write_msg(user_id, "Я не смог найти фотографию в сообщении, отправьте мне фотографию")
            else:
                set_user_image(user_id, dialog_image)
                set_user_state(user_id, "registration_room")
                write_msg(user_id, "Укажите комнату игры (пример: комната-01)")
        elif get_user_state(user_id)[0] == "registration_room":
            set_user_room(user_id, message)
            write_msg(user_id, "Поздравляю, вы успешно зарегистрировались на игру! Ожидайте начало игры. " +
                      "ваша комната: " + get_user_room(user_id))
            set_user_state(user_id, "registration_over")
        else:
            write_msg(user_id, bot.new_message(message))


print("Сервер запущен")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        print(f'Новое сообщение от {event.user_id}', end='')

        bot = VkBot(event.user_id)

        check_message(event)

        print('Текст: ', event.text)
        print("-------------------")

        if get_user(event.user_id) is None:
            register_new_user(event.user_id)
