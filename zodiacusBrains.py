import bs4
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class VkBot:
    """Класс бота. Содержит сбор id пользователя, его имени, а также простейшие команды самого бота, требующиеся
    для приветствия и прощания."""

    # __init__ - публичный метод; self - ссылается на сам объект
    def __init__(self, user_id):
        # Здесь хранится юзер id
        self._USER_ID = user_id
        # Здесь хранится имя пользователя для обращения в сообщениях
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        # Простейшие первичные команды
        self._COMMANDS = ["привет",
                          "ghbdtn",
                          "пока"]

    def _get_user_name_from_vk_id(self, user_id):
        """Метод получает имя пользователя через его id"""
        # Запрашиваем id юзера
        request = requests.get("https://vk.com/id" + str(user_id))
        # парсим
        soup = bs4.BeautifulSoup(request.text, "html.parser")
        user_name = self._clean_all_tag_from_str(soup.findAll("title")[0])
        # Возвращаем имя пользователя
        return user_name.split()[0]

    def read_command_file(self):
        """Метод читает файл с командами бота и вовращает их"""
        # Читаем файл, в котором находятся все команды бота
        commandsFile = open("commands.txt")
        return commandsFile.read()

    def new_message(self, message):
        """Метод обрабатывает сообщения пользователя и возвращает ответ"""
        # Приветствие. Текст сообщения опускаем в нижний регистр, чтобы не быть к нему чувствительными
        if message.lower() == self._COMMANDS[0]:
            return f"Привет, {self._USERNAME}! Я - Зодиакус - твой проводник в мир толкования звёзд.\n " \
                   f"Вот список моих команд:\n" + self.read_command_file()
        # Раскладка клавиатуры
        elif message.lower() == self._COMMANDS[1]:
            return f"Для общения поменяй раскладку клавиатуры - я понимаю только русский 😜"
        # Прощание
        elif message.lower() == self._COMMANDS[2]:
            return f"Пока-пока, {self._USERNAME}!"
        else:
            return f"Я ничего не понял... Помни, что мои команды вводятся через /. " \
                   f"Введи /команды, чтобы посмотреть их список."

    # Метод для очистки от ненужных тэгов
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
