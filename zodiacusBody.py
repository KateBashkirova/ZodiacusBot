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


def write_msg(user_id, message):
    """Функция, посылающая сообщение"""
    random_id = vk_api.utils.get_random_id()
    keyboard = open("keyboard.json", "r", encoding="UTF-8").read()
    # Вызываем метод отправки сообщения с переопределённой клавиатурой
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id, 'keyboard': keyboard})


def switch_sings(argument):
    """
    Функция проверки корректности введённого пользователем знака зодиака и перевода его русского написания в аглийский
    эквивалент
    :param argument введённый пользователем знак зодиака
    :return английский эквивалент или код ошибки -1
    """
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


def _get_personal_horoscope(sign, text):
    """
    Функция вывода персонального гороскопа
    :param sign английский эквивалент введённого пользователем знака зодиака
    :param text русское написание введённого пользователем знака зодиака
    :return текст гороскопа
    """
    # Запрашиваем ответ от страницы с гороскопом конкретного знака
    request = requests.get("https://horo.mail.ru/prediction/" + sign + "/today/")
    # парсим
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    horoscope_txt = soup.find('div', 'article__item article__item_alignment_left article__item_html').getText()
    return "Вот что звёзды рассмотрели для знака " + text.lower() + "👀:\n" + horoscope_txt


# Получение общего гороскопа:
def _get_horoscope_for_all(day):
    """
    Функция получения гороскопа в зависимости от дня недели
    :param day введённый пользователем день, на который нужно искать гороскоп
    :return текст гороскопа
    """
    # Посылаем запрос на страницу с гороскопом
    request = requests.get("https://horo.mail.ru/prediction/" + day + "/")
    # Получаем ответ, парсим
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    # Достаём нужный нам текст
    horoscope_txt = soup.find('div', 'article__item article__item_alignment_left article__item_html').getText()
    return horoscope_txt


def _personal_command(event):
    """
    Функция обработки команды персональный.
    :param event событие
    :return сообщение с персональным гороскопом
    """
    # Спросить о том, для какого знака зодиака искать инфо
    write_msg(event.user_id, "Насчёт какого знака зодиака спрашиваем звёзды?")
    # Бесконечный цикл
    for event in longpoll.listen():
        # Считываем, что ответил пользователь
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                # Если пользователь ввёл команду "стоп"
                if event.text.lower() == "стоп":
                    _stop_command(event)
                    # Бот выходит из цикла обработки команды персональный и готов исполнять другие команды
                    break
                # Если команды "/стоп" не было
                else:
                    # Вызываем метод, который сопоставляет полученное сообщение с существующими ЗЗ
                    sign = switch_sings(event.text.lower())
                    # Словить некорректный ввод. Предупредить и слушать дальше
                    if sign == -1:
                        write_msg(event.user_id, "Такого знака я не знаю... Попробуй ввести ещё раз или "
                                                 "напиши стоп, если не хочешь больше искать гороскопы.")
                    # Если всё введено корректно
                    else:
                        # Вызвать метод нахождения гороскопа по знаку зодиака, вернувшиеся данные вывести
                        write_msg(event.user_id, _get_personal_horoscope(sign, event.text.lower()))
                        write_msg(event.user_id, "Насчёт какого знака зодиака спрашиваем звёзды?\n"
                                                 "Введи стоп, если не хочешь больше искать гороскопы "
                                                 "для конкретного знака.")


def _stop_command(event):
    """Функция обработки команды стоп"""
    write_msg(event.user_id, "Хорошо, больше никаких гороскопов. "
                             "Но я всегда готов сделать что-нибудь другое! "
                             "Введи /команды, чтобы посмотреть список команд.")


def _show_commands(event):
    """Функция обработки команды команды"""
    write_msg(event.user_id, "Вот список моих команд:\n" + bot.read_command_file())


# Основной цикл обработки команд
# Тут реализуется циклическая проверка на наличие какой-либо активности в чате
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно для бота
        if event.to_me:
            # Для вывода в консоли (необязательно)
            print('New message:')
            print(f'For me by: {event.user_id}', end='' + "\n")

            # Инициализируем часть бота из zodiacusBrains.py для обработки первичных и самых лёгких команд
            bot = VkBot(event.user_id)

            # Обработка команд

            # Если получена команда "/персональный"
            if event.text == "персональный":
                _personal_command(event)
            # Если получена команда на просмотр всех команд
            elif event.text.lower() == "команды":
                _show_commands(event)
            # Если запросили гороскоп для всех знаков на текущий день
            elif event.text.lower() == "сегодня":
                write_msg(event.user_id, "Вот что звёзды рассмотрели для всех знаков на сегодня:\n" \
                          + _get_horoscope_for_all("today"))
            # Если запросили гороскоп для всех знаков на следующий день
            elif event.text.lower() == "завтра":
                write_msg(event.user_id, "Вот что звёзды говорят для всех знаков на завтра:\n" \
                          + _get_horoscope_for_all("tomorrow"))
            else:
                # Получаем id юзера, который отправил сообщение, чтобы ответить ему;
                write_msg(event.user_id, bot.new_message(event.text))

            # Для вывода в консоли (необязательно)
            print('Text: ', event.text)
