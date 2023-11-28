import pytest
from bot_realization.function_bot import *

my_id = 253450204

#получение последних новостей
def test_01_outofrange_plus_get_last_news():
    assert get_last_news(100) == "Введите число в нужном диапазоне"

def test_02_outofrange_minus_get_last_news():
    assert get_last_news(-100) == "Введите число в нужном диапазоне"

def test_03_correct_input_into_last_news():
    assert get_last_news(5) != "Введите число в нужном диапазоне"

#получение новостей по теме
url_mk_t1 = 'https://www.mk.ru/politics/'
url_mk_t2 = 'https://www.mk.ru/economics/'
url_mk_t3 = 'https://www.mk.ru/incident/'
url_mk_t4 = 'https://www.mk.ru/sport/'

def test_04_outofrange_plus_get_news():
    assert get_news(url_mk_t1,100) == "Введите число в нужном диапазоне"

def test_05_outofrange_minus_get_news():
    assert get_news(url_mk_t1,-100) == "Введите число в нужном диапазоне"

def test_06_not_outofrange_get_news():
    assert get_news(url_mk_t1, 1) != "Введите число в нужном диапазоне"

def test_07_work_url1_get_news():
    assert get_news(url_mk_t2, 1) != "Введите число в нужном диапазоне"

def test_08_work_url2_get_news():
    assert get_news(url_mk_t3, 1) != "Введите число в нужном диапазоне"

def test_09_work_url3e_get_news():
    assert get_news(url_mk_t4, 1) != "Введите число в нужном диапазоне"

#проверка работы функции проверки времени и диапазона для установки уведомлений
def test_10_allgood_check_vvod():
    assert check_vvod(['12','34','5']) == True

def test_11_hh_wrong_check_vvod():
    assert check_vvod(['56','34','5']) == False

def test_12_hh_check_vvod():
    assert check_vvod(['01','34','5']) == True

def test_13_mm_wrong_check_vvod():
    assert check_vvod(['12','78','5']) == False

def test_14_mm_wrong_minus_check_vvod():
    assert check_vvod(['12','-10','5']) == False

def test_15_count_wrong_check_vvod():
    assert check_vvod(['12','34','34']) == False