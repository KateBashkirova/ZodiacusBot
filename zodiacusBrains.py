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
        self._COMMANDS = ["привет",
                          "/сегодня",
                          "/завтра",
                          "ghbdtn",
                          "пока"]

    #Метод, получающий имя пользователя через его id
    def _get_user_name_from_vk_id(self, user_id):
        # Запрашиваем id юзера
        request = requests.get("https://vk.com/id" + str(user_id))
        # парсим
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        # Возвращаем имя пользователя
        return user_name.split()[0]


    # Метод, обрабатывающий сообщения пользователя и возвращающий ответ
    def new_message(self, message):

        # Приветствие. Текст сообщения поднимаем в верхний регистр, чтобы пользователь мог писать и так, и так
        if message.lower() == self._COMMANDS[0]:
            return f"Привет, {self._USERNAME}! Я - Зодиакус - твой проводник в мир толкования звёзд.\n Вот список моих команд:\n" \
                   f"/команды - показать все команды;\n" \
                   f"/сегодня - гороскоп для всех знаков на сегодня;\n" \
                   f"/завтра - гороскоп для всех знаков на завтра;\n" \
                   f"/персональный - гороскоп для конкретного знака зодиака."

        # Гороскопы
        # Гороскоп на сегодня
        elif message.lower() == self._COMMANDS[1]:
            return f"Вот что звёзды предвещают для всех знаков на сегодня: \n"+self._get_today_horoscope()
        # Гороскоп на завтра
        elif message.lower() == self._COMMANDS[2]:
            return f"Вот что звёзды разглядели для всех знаков на завтра: \n"+self._get_tomorrow_horoscope()
        # Раскладка
        elif message.lower() == self._COMMANDS[3]:
            return f"Для общения поменяй раскладку клавиатуры - я понимаю только русский 😜"
        # Прощание. Текст сообщения поднимаем в верхний регистр, чтобы пользователь мог писать и так, и так
        elif message.lower() == self._COMMANDS[4]:
            return f"Пока-пока, {self._USERNAME}!"
        else:
            return f"Я ничего не понял..."

    # Получение гороскопа на сегодня:
    def _get_today_horoscope(self):
        # Посылаем запрос на страницу с гороскопом
        request = requests.get("https://horo.mail.ru/prediction/today/")
        # Получаем ответ, парсим
        soup = bs4.BeautifulSoup(request.text, "html.parser")
        # Достаём нужный нам текст
        headlines = soup.find('div', 'article__item article__item_alignment_left article__item_html').getText()
        print(headlines)
        # Возвращаем текст
        return (headlines)

    # Получение гороскопа на завтра:
    def _get_tomorrow_horoscope(self):
        request = requests.get("https://horo.mail.ru/prediction/tomorrow/")
        soup = bs4.BeautifulSoup(request.text, "html.parser")
        headlines = soup.find('div', 'article__item article__item_alignment_left article__item_html').getText()
        print(headlines)
        return (headlines)



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
