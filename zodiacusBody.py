import bs4
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from zodiacusBrains import VkBot

# API токен сообщества
mytoken = 'b8bfa52f5f8b7f2f5d9c787032a5d4b9aac5f9f06e82b3b736ce3a5315cb6bcccb1a725805a2ec024147c'

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=mytoken)
longpoll = VkLongPoll(vk)


# Функция посылающая сообщение
# Получает на вход id юзера, которому отправит сообщение, и само сообщение
def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


# Метод выбора знака зодиака
def switch_sings(argument):
    return {
        "овен": "aries",
        "телец": "taurus",
        "близнецы": "gemini",
        "рак": "cancer",
        "лев": "leo",
        "дева": "virgo",
        "весы": "libra",
        "скорпион": "scorpio",
        "стрелец": "sagittarius",
        "козерог": "capricorn",
        "водолей": "aquarius",
        "рыбы": "pisces",
    }.get(argument, -1)


# Метод, который запрашивает гороскоп в зависимости от указанного знака зодиака
def _get_pernsonal_horoscope(sign, text):
    # Запрашиваем ответ от страницы с гороскопом конкретного знака
    request = requests.get("https://horo.mail.ru/prediction/" + sign + "/today/")
    # парсим
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    horoscopeTxt = soup.find('div', 'article__item article__item_alignment_left article__item_html').getText()
    return ("Вот что звёзды рассмотрели для знака "+text.lower()+"👀:\n" + horoscopeTxt)


# Основной цикл
for event in longpoll.listen():  # Тут реализуется циклическая проверка на наличие какой-то активности
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно для бота
        if event.to_me:
            # Для вывода в консоли (необязательно)
            print('New message:')
            print(f'For me by: {event.user_id}', end='' + "\n")

            bot = VkBot(event.user_id)

            if event.text == "/персональный":
                write_msg(event.user_id, "Насчёт какого знака зодиака спрашиваем звёзды?")
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        # Если оно для бота
                        if event.to_me:
                            # Если пользователь ввёл команду "/стоп"
                            if event.text.lower() == "/стоп":
                                write_msg(event.user_id, "Хорошо, больше никаких гороскопов. "
                                                         "Но я всегда готов сделать что-нибудь другое! "
                                                         "Введи /команды, чтобы посмотреть список команд.")
                                break  # выходим из цикла
                            else:
                                # Вызываем метод, который сопоставляет введённый ЗЗ с имеющимися и возвращает гороскоп
                                sign = switch_sings(event.text.lower())
                                if sign == -1:
                                    write_msg(event.user_id, "Ещё раз так сделаешь - по IP вычислю. Тебя попросили знак ввести\n"
                                                             "Напиши /стоп, если не хочешь больше напрягаться")
                                else:
                                    # Вернувшееся значение выводим в сообщение пользователю
                                    write_msg(event.user_id, _get_pernsonal_horoscope(sign, event.text.lower()))
                                    write_msg(event.user_id, "Насчёт какого знака зодиака спрашиваем звёзды?\n"
                                                             "Введи /стоп, если не хочешь больше искать гороскопы"
                                                             " для конкретного знака.")
            elif event.text == "/команды":
                write_msg(event.user_id, "Вот список моих команд:\n" \
                   f"/сегодня - гороскоп для всех знаков на сегодня;\n" \
                   f"/завтра - гороскоп для всех знаков на завтра;\n" \
                   f"/персональный - гороскоп для конкретного знака зодиака.")
            else:
                # Получаем id юзера, который отправил сообщение, чтобы ответить ему;
                write_msg(event.user_id, bot.new_message(event.text))

            # Для вывода в консоли (необязательно)
            print('Text: ', event.text)
