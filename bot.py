import bs4
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from zodiacusBrains import VkBot

# API токен сообщества
mytoken = 'b8bfa52f5f8b7f2f5d9c787032a5d4b9aac5f9f06e82b3b736ce3a5315cb6bcccb1a725805a2ec024147c'


# Функция посылающая сообщение
# Получает id юзера, которому отправит сообщение, и само сообщение
def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


# Авторизуемся как сообщество
vk = vk_api.VkApi(token=mytoken)
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen(): # Тут реализуется циклическая проверка на наличие какой-то активности
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            # Для вывода в консоли (необязательно)
            print('New message:')
            print(f'For me by: {event.user_id}', end='')

            # Кому отправляем, что отправляем
            bot = VkBot(event.user_id)
            write_msg(event.user_id, bot.new_message(event.text))

            # Для вывода в консоли (необязательно)
            print('Text: ', event.text)