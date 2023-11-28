#3 вариант. Чат-бот для получения новостей (новостной агрегатор):
#Вы сами выбираете источник новости (какой-то сайт, хоть РБК).
#Бот может прислать тексты последних 1-10 новостей (настраивает пользователь).
#Бот может присылать новосте по теме (задать или выбрать из списка)

#Способен присылать новости раз в сутки (другой период) в определенное время
#(можно настраивать). Нужны настройки, чтобы пользователь сам говорил,
#когда присылать, и сколько новостей (от 1 до 20).

#дополнительно реализована возможность выбирать количество
#новостей, которое пользователь получит по ранее выбранной теме

import vk, vk_api
import requests
import schedule, time, threading
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bs4 import BeautifulSoup

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from function_bot import *

keyboard_start = VkKeyboard(one_time = True)
keyboard_start.add_button('Меню', color = VkKeyboardColor.PRIMARY)
keyboard_start.add_line()
keyboard_start.add_button('Уведомления', color = VkKeyboardColor.SECONDARY)

keyboard_error = VkKeyboard(one_time = True)
keyboard_error.add_button('Авторизация', color = VkKeyboardColor.PRIMARY)

keyboard1 = VkKeyboard(one_time = True)
keyboard1.add_button('Новости по теме', color = VkKeyboardColor.PRIMARY)
keyboard1.add_button('Последние новости', color = VkKeyboardColor.POSITIVE)
keyboard1.add_line()
keyboard1.add_button('Начало', color = VkKeyboardColor.SECONDARY)

#блок новости по теме
keyboard2 = VkKeyboard(one_time = True)
keyboard2.add_button('Политика', color = VkKeyboardColor.POSITIVE)
keyboard2.add_button('Экономика', color = VkKeyboardColor.POSITIVE)
keyboard2.add_line()
keyboard2.add_button('Происшествия', color = VkKeyboardColor.POSITIVE)
keyboard2.add_button('Спорт', color = VkKeyboardColor.POSITIVE)
keyboard2.add_line()
keyboard2.add_button('Начало', color = VkKeyboardColor.SECONDARY)

notif_keyboard = VkKeyboard(one_time=True)
notif_keyboard.add_button('Установить', color=VkKeyboardColor.POSITIVE)
notif_keyboard.add_button('Отключить', color=VkKeyboardColor.NEGATIVE)
notif_keyboard.add_line()
notif_keyboard.add_button('Начало', color = VkKeyboardColor.SECONDARY)

group_key = "vk1.a.xblw2f7PIBa5Fj4oRzs9mjoeGUO_aSCgo1S4ZosZWrIo59p0YYBjdh3vVn_r5uH-SdrPUv16Ldjxm0MZ-76ubIzMzXQdNPwkVSh_AnrAD2fb_FYGiswFgThrKmAx-9pgYXrYtuHsgp1mP9O5dwPFcPN02TBHIv6uNZz4yWg9EUYc4A30VuebsFd1SPuTzyLuFHIQwVIlzYZlwt2jJCSl-Q"
key_m = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjgxMTM2NCIsInVudGlsIjoxNjk2MzQ2OTc2MTMwMTc4MTY5fQ.VnbbWQByyUf-OJbl5b2oRqMdAdh1Sde28aOqT1i6BI1Oy9mbeSzkovaEjJuT7V800vzdZL9zenL-spVCtsVhCA"

vk_session = vk_api.VkApi(token = group_key)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

#https://www.mk.ru
#title = b.select('.news-listing__day-list .news-listing__item')
#url = b.find('a', class_='news-listing__item-link').get('href')
#title = b.select('.article-listing__day-list .listing-preview__title')
#url = b.find('a', class_='listing-preview__content').get('href')

def get_last_news_for_shedule(n, user_id_id):
    if(users_dict[user_id_id].uved == 1):
        vk.messages.send(
            user_id= user_id_id,
            random_id=get_random_id(),
            message=get_last_news(n))

#работа с уведомлениями

def notif_thread():
    while True:
        schedule.run_pending()
        time.sleep(60)
threading.Thread(target=notif_thread).start()

class Users:
    uved = 0
    # 0-не надо, 1-надо, 10 - установка
    uved_count = 0
    news = -1
    # 1-последние, 2-по теме, -1-дефолт
    def __init__(self, user_id):
        self.user_id = user_id

url_mk_t = 'https://www.mk.ru/politics/'

users_dict = {}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        if event.user_id in users_dict:
            #уведомления
            if event.text.startswith('Уведомления'):
                vk.messages.send(keyboard = notif_keyboard.get_keyboard(),
                    key = (key_m),
                    server = ("https://lp.vk.com/whp/222811364"),
                    ts = ("14"),
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    message = "Настройте уведомления")

            elif event.text.startswith('Установить'):
                if(users_dict[event.user_id].uved == 1):
                    vk.messages.send(keyboard=notif_keyboard.get_keyboard(),
                        key=(key_m),
                        server=("https://lp.vk.com/whp/222811364"),
                        ts=("14"),
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="У вас уже стоят уведомления - отключите их, чтобы сменить время")
                else:
                    users_dict[event.user_id].uved = 10
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Введите параметры для уведомлений в формате \nчасы:минуты:колво-уведомлений(1-20) \nhh:mm:n')

            elif event.text.startswith('Отключить'):
                users_dict[event.user_id].uved = 0
                vk.messages.send(
                    keyboard=keyboard_start.get_keyboard(),  # меню
                    key=(key_m),
                    server=("https://lp.vk.com/whp/222811364"),
                    ts=("14"),
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Уведомления успешно отключены')

            #меню
            elif event.text.startswith('Меню'):
                users_dict[event.user_id].news = 0
                vk.messages.send(keyboard = keyboard1.get_keyboard(), #по теме, последние и начало
                    key = (key_m),
                    server = ("https://lp.vk.com/whp/222811364"),
                    ts = ("14"),
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    message = "Выберите какие новости хотите получить")

            #блок новости по теме
            elif event.text.startswith('Новости по теме'):
                users_dict[event.user_id].news = 2
                vk.messages.send(keyboard=keyboard2.get_keyboard(), #темы
                    key=(key_m),
                    server=("https://lp.vk.com/whp/222811364"),
                    ts=("14"),
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message = "Выберите тему, по которой хотите получить новости")

            elif ( (event.text.startswith('Политика') or event.text.startswith('Экономика')
                  or event.text.startswith('Происшествия') or event.text.startswith('Спорт')) and users_dict[event.user_id].news == 2):
                if event.text.startswith('Политика'):
                    url_mk_t = 'https://www.mk.ru/politics/'
                elif event.text.startswith('Экономика'):
                    url_mk_t = 'https://www.mk.ru/economics/'
                elif event.text.startswith('Происшествия'):
                    url_mk_t = 'https://www.mk.ru/incident/'
                else:
                    url_mk_t = 'https://www.mk.ru/sport/'
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Введите число от 1 до 10 - сколько новостей вы хотите получить")

            #блок последние новости
            elif event.text.startswith('Последние новости'):
                users_dict[event.user_id].news = 1
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Введите число от 1 до 10 - сколько новостей вы хотите получить")

            elif event.text.isdigit():
                    #последние новости
                    if (users_dict[event.user_id].news == 1):
                        if get_last_news(int(event.text)) != "Введите число в нужном диапазоне":
                            users_dict[event.user_id].news = 0
                            vk.messages.send(keyboard=keyboard1.get_keyboard(),  #возвращнение - по теме, последние и начало
                                key=(key_m),
                                server=("https://lp.vk.com/whp/222811364"),
                                ts=("14"),
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message=get_last_news(int(event.text)))
                        else:
                            vk.messages.send(keyboard=keyboard1.get_keyboard(),
                                key=(key_m),
                                server=("https://lp.vk.com/whp/222811364"),
                                ts=("14"),
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message=get_last_news(int(event.text)))

                    # новости по теме
                    elif (users_dict[event.user_id].news == 2):
                        if get_news(url_mk_t, int(event.text)) != "Введите число в нужном диапазоне":
                            users_dict[event.user_id].news = 0
                            vk.messages.send(keyboard=keyboard1.get_keyboard(),  #возвращнение - по теме, последние и начало
                                key=(key_m),
                                server=("https://lp.vk.com/whp/222811364"),
                                ts=("14"),
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message=get_news(url_mk_t, int(event.text)))
                        else:
                            vk.messages.send(keyboard=keyboard1.get_keyboard(),
                                key=(key_m),
                                server=("https://lp.vk.com/whp/222811364"),
                                ts=("14"),
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message=get_news(url_mk_t, int(event.text)))

                    #вообще случайно цицру написал
                    else:
                        vk.messages.send(
                            keyboard=keyboard_start.get_keyboard(),  #меню
                            key=(key_m),
                            server=("https://lp.vk.com/whp/222811364"),
                            ts=("14"),
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Нажмите на кнопку, чтобы продолжить работу с ботом или включить уведомления")

            #уведомления
            elif (users_dict[event.user_id].uved == 10):
                message = event.text
                message_list = message.strip(' ').split(':')
                #если все ок добавляем
                if (len(message_list) == 3 and len(message_list[0]) == len(message_list[1]) == 2 and 1 <= len(message_list[2]) <= 2 and check_vvod(message_list)):
                    users_dict[event.user_id].uved_count = int(message_list[2])
                    #включение уведомлений конкретному пользователю
                    schedule.every().day.at(message[0:5]).do(get_last_news_for_shedule, users_dict[event.user_id].uved_count, event.user_id)
                    users_dict[event.user_id].uved = 1
                    vk.messages.send(
                        keyboard=keyboard_start.get_keyboard(),  # меню
                        key=(key_m),
                        server=("https://lp.vk.com/whp/222811364"),
                        ts=("14"),
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Уведомления успешно включены")

                #иначе просим пройти все заново
                else:
                    users_dict[event.user_id].uved = 0
                    vk.messages.send(
                        keyboard=keyboard_start.get_keyboard(),  #меню
                        key=(key_m),
                        server=("https://lp.vk.com/whp/222811364"),
                        ts=("14"),
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Ввод неверный, попробуйте еще раз")


            else:
                users_dict[event.user_id].uved = 0
                users_dict[event.user_id].news = 0
                vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                    key=(key_m),
                    server=("https://lp.vk.com/whp/222811364"),
                    ts=("14"),
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Нажмите на кнопку, чтобы продолжить работу с ботом или включить уведомления")

        # добавление нового юзера
        else:
            users_dict[event.user_id] = Users(event.user_id)
            vk.messages.send(keyboard=keyboard_error.get_keyboard(),
                key=(key_m),
                server=("https://lp.vk.com/whp/222811364"),
                ts=("14"),
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Нажмите на кнопку, чтобы начать работу с ботом")
