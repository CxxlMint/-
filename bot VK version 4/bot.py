# 2453f743a9720b082acd93fbecb88e9fde7a4d737fbd4968fb89d00f54d305ad651ecfafc7f90b0d9f3ae

from vk_bot import VkBot
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


def get_user_password(user_id):
    cmd = "SELECT user_password FROM user_info WHERE user_id=%d" % user_id
    c.execute(cmd)
    return c.fetchone()[0]


# регистрация нового пользователя
def register_new_user(user_id):
    cmd = "INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id
    c.execute(cmd)
    conn.commit()
    cmd = "INSERT INTO user_info(user_id, user_password, is_dead) VALUES (%d, '%s', 0)" % (user_id,
                                                                                           generate_user_password())
    c.execute(cmd)
    conn.commit()
    cmd = "INSERT INTO game_adventure(user_id, user_save, user_progress, user_skill_1, user_skill_2, user_skill_3," \
          " user_in_game) VALUES (%d, 0, 0, 0, 0, 0, 0)" % user_id
    c.execute(cmd)
    conn.commit()


# показывает прогресс игрока в приключении
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
    return c.fetchone()


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
    return c.fetchone()


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


def send_message_about_jertva_to_room(room):
    cmd = "SELECT user_id, target_id FROM user_info WHERE user_room='%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    for item in result:
        image = generate_message_about_jertva(item[1])
        message = "Ваша цель:"
        vk.method('messages.send', {'user_id': item[0], 'message': message, 'attachment': image, 'random_id': random.randint(0, 2048)})


# генератор жертвы
def generate_jertva(room):
    cmd = "SELECT user_id FROM user_info WHERE user_room='%s'" % room
    c.execute(cmd)
    result = c.fetchall()
    for item in result:
        if result.index(item) != len(result) - 1:
            jertva = result[result.index(item) + 1]
            cmd = "UPDATE user_info SET target_id=%d WHERE user_id=%d" % (jertva[0], item[0])
            c.execute(cmd)
            conn.commit()
        else:
            cmd = "UPDATE user_info SET target_id=%d WHERE user_id=%d" % (result[0][0], item[0])
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


# написание сообщения
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


# обработка сообщений
def check_message(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id
    # if cur_event.text[0] == "/":
    # write_msg(event.user_id, commander.do(message[1::]))

    if message.lower() == "сначала игра приключение":
        set_user_progress(user_id, "0")

    if message.lower() == "игра приключение":
        set_user_in_game(user_id, "1")
        write_msg(user_id, bot.new_message(message))

        if int(get_user_progress(user_id)[0]) == 0:
            write_msg(user_id, "выберите рассу из предложенного списка: Человек, Эльф, Орк")

    elif int(get_user_in_game(user_id)[0]) == 1:

        if message.lower() == "выход игра приключение":
            set_user_in_game(user_id, "0")
            write_msg(user_id, "Возвращайтесь скорее! Вас ждут приключения!")

        elif int(get_user_progress(user_id)[0]) == 0:
            if message.lower() == "человек":
                set_user_race(user_id, "человек")
                set_user_skill_1(user_id, "2")
                set_user_skill_2(user_id, "2")
                set_user_skill_3(user_id, "2")
                set_user_progress(user_id, "1")
            elif message.lower() == "эльф":
                set_user_race(user_id, "эльф")
                set_user_skill_1(user_id, "1")
                set_user_skill_2(user_id, "2")
                set_user_skill_3(user_id, "3")
                set_user_progress(user_id, "1")
            elif message.lower() == "орк":
                set_user_race(user_id, "орк")
                set_user_skill_1(user_id, "3")
                set_user_skill_2(user_id, "2")
                set_user_skill_3(user_id, "1")
                set_user_progress(user_id, "1")
            else:
                write_msg(user_id, "Я не понял ваши слова, выберите рассу из предложенного списка: Человек, Эльф, Орк")

        elif int(get_user_progress(user_id)[0]) == 1:
            write_msg(user_id, "отлично, ваша расса теперь " + str(get_user_race(user_id)[0])
                      + ".Ваша сила, красноречие и сила магии равны: " + str(get_user_skill_1(user_id)[0])
                      + ", " + str(get_user_skill_2(user_id)[0]) + ", " + str(get_user_skill_3(user_id)[0])
                      + ". Если вы захотите всё изменить напишитe: сначала игра приключение")
            write_msg(user_id, "Да начнутся приключения!")
            set_user_progress(user_id, "2")
        elif int(get_user_progress(user_id)[0]) == 2:
            write_msg(user_id, "Ваши приключения скоро начнутся, ожидайте.")
    elif get_user_state(user_id) is None:
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
        if get_user_state(user_id)[0] == "registration_over":
            if cur_event.text == 'смена стадии ' + str(get_user_room(user_id)) + " " + str(
                    get_password_room(get_user_room(user_id))):
                a = message.split(' ')
                set_game_stage(1, a[2])
                send_message_to_room("Внимание, игра началась!", a[2])
                send_message_to_room("Для того, чтобы убить жертву, вам нужно написать мне её пароль. Чтобы узнать свой пароль напишите: мой пароль.")
                generate_jertva(a[2])
                send_message_about_jertva_to_room(a[2])
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
                write_msg(user_id, "Укажите комнату игры (пример: комната-01)")
        elif get_user_state(user_id)[0] == "registration_room":
            print(str(message), get_rooms())
            if str(message) in get_rooms() is True:
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
def check_message_on_stage_one(cur_event):
    message = cur_event.text
    user_id = cur_event.user_id
    # if cur_event.text[0] == "/":
    # write_msg(event.user_id, commander.do(message[1::]))
    if get_user_state(user_id) is None:
        write_msg(user_id, bot.new_message(message))
    if cur_event.text == 'смена стадии ' + str(get_user_room(user_id)) + " " + str(
            get_password_room(get_user_room(user_id))):
        a = message.split(' ')
        cur_stage = get_game_stage(a[2])
        set_game_stage(int(cur_stage) + 1, a[2])
        print(cur_stage + 1)
        if cur_stage + 1 == 1:
            send_message_to_room("Внимание, игра началась!", a[2])
            write_msg(user_id,
                      "Для того, чтобы убить жертву, вам нужно написать мне её пароль. Ваш пароль: " + get_user_password(
                          user_id) + ".")
        elif cur_stage + 1 == 2:
            send_message_to_room("Внимание, игра окончена, идет подсчет итогов, ожидайте!", a[2])
        else:
            send_message_to_room("Внимание, итог игры готов, победители: " + ".", a[2])
    elif cur_event.text.lower() == 'регистрация киллер':
        write_msg(user_id, "Регистрация невозможна, вы уже зарегестрированы")
    elif cur_event.text.lower() == 'перегистрация киллер':
        write_msg(user_id, "Перегистрация невозможна, вы находитесь в игре")
    else:
        if check_kill(user_id, message):
            new_target = change_jertva(user_id)
            image = generate_message_about_jertva(new_target)
            vk.method('messages.send', {'user_id': user_id,
                                        'message': "Поздравляем, вы убили свою жертву, вот данные о следующей жертве:",
                                        'attachment': image, 'random_id': random.randint(0, 2048)})
        write_msg(user_id, bot.new_message(message))


print("Сервер запущен")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        print(f'Новое сообщение от {event.user_id}', end='')

        if get_user(event.user_id) is None:
            register_new_user(event.user_id)

        bot = VkBot(event.user_id)

        check_message(event)

        print('Текст: ', event.text)
        print("-------------------")
