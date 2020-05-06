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


def switch_sings(argument):
    return {
        "овен": 1,
        "телец": 2,
        "близнецы": 3,
        "рак": 4,
        "лев": 5,
        "дева": 6,
        "веса": 7,
        "скорпион": 8,
        "стрелец": 9,
        "козерог": 10,
        "водолей": 11,
        "рыбы": 12,
    }.get(argument, "Вы неверно написали знак зодиака. Попробуйте ещё раз.") # выведет -1, если аргумента нет


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
                write_msg(event.user_id, "Введите запрос:")
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        # Если оно для бота
                        if event.to_me:
                            write_msg(event.user_id, switch_sings(event.text))
                            break  # выходим из цикла
            else:
                # Получаем id юзера, который отправил сообщение, чтобы ответить ему;
                write_msg(event.user_id, bot.new_message(event.text))

            # Для вывода в консоли (необязательно)
            print('Text: ', event.text)
