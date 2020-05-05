import bs4
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class VkBot:
    def __init__(self, user_id):
        # Здесь будет храниться юзер id
        self._USER_ID = user_id
        # Здесь будет храниться имя пользователя, получаемое функцией _get_user_name_from_vk_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        # Список команд бота
        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ГОРОСКОП", "ПОКА"]

    def _get_user_name_from_vk_id(self, user_id):
        # Запрашиваем id юзера
        request = requests.get("https://vk.com/id" + str(user_id))
        # парсим
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        # Возвращаем имя пользователя
        return user_name.split()[0]

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

    # Метод, обрабатывающий сообщения пользователя и возвращающий ответ
    def new_message(self, message):

        # Приветствие. Текст сообщения поднимаем в верхний регистр, чтобы пользователь мог писать и так, и так
        if message.upper() == self._COMMANDS[0]:
            return f"Привет, {self._USERNAME}! Я - Зодиакус - твой проводник в мир толкования звёзд. Напиши гороскоп," \
                   f" чтобы посмотреть, что планеты уготовили на сегодня"

        # Прощание. Текст сообщения поднимаем в верхний регистр, чтобы пользователь мог писать и так, и так
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"
            # Гороскоп
        elif message.upper() == self._COMMANDS[2]:
            return f"Посмотрим, что звёзды предвещают на сегодня... \n"+self._get_today_horoscope()
        else:
            return f"Я ничего не понял..."

    # Получение гороскопа:
    def _get_today_horoscope(self):
        request = requests.get("https://horo.mail.ru/")
        soup = bs4.BeautifulSoup(request.text, "html.parser")
        headlines = soup.find('div', 'article__item article__item_alignment_left article__item_html').getText()
        print(headlines)
        return (headlines)

