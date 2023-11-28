from bs4 import BeautifulSoup
import requests

class News:
    def __init__(self, title, link):
        self.title = title
        self.link = link
    def get_news_text(self):
        return(f"{self.title} {self.link}\n\n")

def check_vvod(message: list):
    num1 = int(message[0])
    num2 = int(message[1])
    num3 = int(message[2])
    if 0 <= num1 <= 23 and 0 <= num2 <= 59 and 0 <= num3 <= 20:
        return True
    else:
        return False

def get_last_news(n):
    if 1 <= n and n <= 10:
        news = ''
        request = requests.get('https://www.mk.ru')
        b = BeautifulSoup(request.text, "html.parser")
        title = b.select('.news-listing__day-list .news-listing__item')
        url = b.select('[class *= "news-listing__item-link"]')
        for i in range(n):
            another_new = News(title[i].getText(), url[i].get("href"))
            news += another_new.get_news_text() + '\n'
        return(news)
    else:
        return "Введите число в нужном диапазоне"

def get_news(url_mk, n):
    if 1 <= n and n <= 10:
        news = ''
        request = requests.get(url_mk)
        b = BeautifulSoup(request.text, "html.parser")
        title = b.select('.article-listing__day-list .listing-preview__title')
        url = b.select('[class *= "listing-preview__content"]')
        for i in range(n):
            another_new = News(title[i].getText(), url[i].get("href"))
            news += another_new.get_news_text() + '\n'
        return(news)
    else:
        return "Введите число в нужном диапазоне"