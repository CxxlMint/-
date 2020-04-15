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
    cmd = "INSERT INTO user_info(user_id, user_password) VALUES (%d, '%s')" % (user_id, generate_user_password())
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


# написание сообщения
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


# обработка сообщений
def check_message(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id
    if cur_event.text[0] == "/":
        write_msg(event.user_id, commander.do(message[1::]))
    elif message == "регистрация_киллер":
        write_msg(user_id, bot.new_message(message))
        set_user_state(user_id, "registration")
    else:
        write_msg(user_id, bot.new_message(message))


# Авторизация
vk = vk_api.VkApi(token=config.token)
# Работа с сообщениями
longpoll = VkLongPoll(vk)
commander = Commander()
print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        print(f'New message from {event.user_id}', end='')

        bot = VkBot(event.user_id)

        check_message(event)

        print('Text: ', event.text)
        print("-------------------")

        if get_user(event.user_id) is None:
            register_new_user(event.user_id)
