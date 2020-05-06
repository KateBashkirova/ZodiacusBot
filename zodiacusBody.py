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
    }.get(argument, "Вы неверно написали знак зодиака. Попробуйте ещё раз.")  # выведет -1, если аргумента нет


 #Метод, получающий гороскоп по конкретному знаку зодиака
def _get_personal_horoscope(sign):
    # Запрашиваем id юзера
    request = requests.get("https://horo.mail.ru/prediction/"+sign+"/today/")
    # парсим
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    headlines = soup.find('div', 'article__item article__item_alignment_left article__item_html').getText()
    return (headlines)


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
                write_msg(event.user_id, "Введите знак зодиака:")
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        # Если оно для бота
                        if event.to_me:
                            # Вызываем метод, который сопоставляет введённый ЗЗ с имеющимися и возвращает гороскоп
                            sign = switch_sings(event.text.lower())
                            # Вернувшееся значение выводим в сообщение пользователю
                            write_msg(event.user_id, _get_personal_horoscope(sign))
                            break  # выходим из цикла
            else:
                # Получаем id юзера, который отправил сообщение, чтобы ответить ему;
                write_msg(event.user_id, bot.new_message(event.text))

            # Для вывода в консоли (необязательно)
            print('Text: ', event.text)
