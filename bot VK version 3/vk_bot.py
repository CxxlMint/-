import bs4 as bs4
import requests, random

class VkBot:
    def __init__(self, user_id):
        print("\nСоздан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "!ПОГОДА", "!ВРЕМЯ", "ПОКА", "!КОМАНДЫ", "!ЧИСЛО", '!МОНЕТКА', 'РЕГИСТРАЦИЯ КИЛЛЕР']

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        return user_name.split()[0]

    def new_message(self, message):
        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}! " + str(
                random.choice(['&#128521;', '&#128524;', '&#9995; &#128519;']))
        # Погода
        elif message.upper() == self._COMMANDS[1]:
            return self._get_weather()
        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()
        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"
        elif message.upper() == self._COMMANDS[4]:
            return f"Список команд:\n" \
                   f"!Погода - для просмотра погоды &#9728;\n" \
                   f"!Время - для просмотра времени &#127763;\n" \
                   f"!Число - генерация рандомного числа &#128290;\n" \
                   f"!Монетка - подбросить монетку (орел/решка) &#127922;"
        elif message.upper()[0:6] == self._COMMANDS[5]:
            if len(message.split(' ')) != 3:
                return f"Неверный синтаксис, надо вводить так:\n" \
                       f"!Число [от] [до]"
            else:
                if int(message.split(' ')[1]) > int(message.split(' ')[2]):
                    return f"Первое число больше второго &#128530;"
                else:
                    return f"Ваше число: " + str(random.randint(int(message.split(' ')[1]), int(message.split(' ')[2])))
        elif message.upper() == self._COMMANDS[6]:
            return f"Иии выпадает! " + random.choice(['Орёл', 'Решка']) + ' ' + str(
                random.choice(['&#127773;', '&#128516;', '&#128527;', '&#128517;']))
        elif message.upper() == self._COMMANDS[7]:
            return "отлично, для регитрации на игру отправьте свою фотографию, чтобы другие игроки смогли вас найти"
        else:
            return "Не понимаю о чем вы... &#128530;\n Для списка команд напишите:\n" \
                   "!команды"

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result

    @staticmethod
    def _get_weather(city: str = "санкт-петербург") -> list:
        request = requests.get("https://sinoptik.com.ru/погода-" + city)
        b = bs4.BeautifulSoup(request.text, "html.parser")
        p3 = b.select('.temperature .p3')
        weather1 = p3[0].getText()
        p4 = b.select('.temperature .p4')
        weather2 = p4[0].getText()
        p5 = b.select('.temperature .p5')
        weather3 = p5[0].getText()
        p6 = b.select('.temperature .p6')
        weather4 = p6[0].getText()
        result = ''
        result = result + ('Утром :' + weather1 + ' ' + weather2) + '\n'
        result = result + ('Днём :' + weather3 + ' ' + weather4) + '\n'
        temp = b.select('.rSide .description')
        weather = temp[0].getText()
        result = result + weather.strip()
        return result
