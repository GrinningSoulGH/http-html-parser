import requests
import sys
from bs4 import BeautifulSoup

def get_html(telephone_number):
    request = requests.get(f"http://www.neberitrubku.ru/nomer-telefona/{telephone_number}")
    if request.status_code == 200:
        return request.text
    else:
        return False

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def get_ratings(parsed_html):
    ratings = parsed_html.find("div", class_ = "ratings")
    if ratings:
        string_ratings = list(map(lambda x: x.string, ratings.find_all("li")))
        return string_ratings
    else:
        return False

def get_categories(parsed_html):
    categories = parsed_html.find("div", class_ = "categories")
    if categories:
        string_categories = list(map(lambda x: x.string, categories.find_all("li")))
        return string_categories
    else:
        return False

def get_information(parsed_html):
    information = dict.fromkeys(['Оценки', 'Категории'])
    ratings = get_ratings(parsed_html)
    if ratings:
        information['Оценки'] = {}
        for rating in ratings:
            split_rating = rating.split()
            information['Оценки'].update({split_rating[1].capitalize(): split_rating[0][:-1]})
    else:
        information['Оценки'] = 'Оценок пока нет'
        
    categories = get_categories(parsed_html)
    if categories:
        information['Категории'] = {}
        for category in categories:
            split_category = category.split()
            information['Категории'].update({split_category[1].capitalize(): split_category[0][:-1]})
    else:
        information['Категории'] = 'Категории пока отсутствуют'
    return information