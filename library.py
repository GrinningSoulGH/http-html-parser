import aiohttp
from aiohttp import web
import json
from bs4 import BeautifulSoup

class Server:
    def __init__(self):
        app = web.Application()
        app.add_routes([web.get('/one', self.get),
                        web.post('/one', self.post)])
        web.run_app(app)

    async def get(self, request):
        telephone_number = request.query['number']
        response_dict = await run(telephone_number)
        return web.json_response(response_dict)

    async def post(self, request):
        telephone_number = await request.text()
        print(telephone_number)
        response_dict = await run(telephone_number)
        print(response_dict)
        return web.json_response(response_dict)

async def get_one(number):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/one', params = {'number': f'{number}'}) as resp:
            with open('json2.txt', 'w') as outfile:
                json.dump(await resp.json(), outfile, ensure_ascii= False, indent=4)

async def post_one(number):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/one', data = f'{number}') as resp:
            with open('json2.txt', 'w') as outfile:
                json.dump(await resp.json(), outfile, ensure_ascii= False, indent=4)

async def post_many(data = list(range(84959999999, 84960010000))):
    all_numbers_dict = {}
    async with aiohttp.ClientSession() as session:
        for number in data:
            async with session.post('http://localhost:8080/one', data = f'{number}') as resp:
                all_numbers_dict[f'{number}'] = await resp.json()
        with open('json2.txt', 'w') as outfile:
            json.dump(all_numbers_dict, outfile, ensure_ascii= False, indent=4)

async def get_html(telephone_number, mode = 'default'):
    if mode == 'default':
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://www.neberitrubku.ru/nomer-telefona/{telephone_number}") as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return False
    elif mode == 'test':
        html = open("html_test.html", "r").read()
        return html

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def get_classes():
    classes = []
    print('Input classes to pull lists from(to end input "end"):')
    while True:
        input_string = input().lower()
        if input_string == 'end':
            break
        else:
            classes.append(input_string)
    return classes

def get_class_lists(parsed_html, _class):
    _class_tag = parsed_html.find("div", class_ = _class)
    if _class_tag:
        string_lists = list(map(lambda x: x.string, _class_tag.find_all("li")))
        return string_lists
    else:
        return False

def get_information(parsed_html, classes = ['ratings', 'categories']):
    information = dict.fromkeys(classes)
    for _class in classes:
        _class_list_strings = get_class_lists(parsed_html, _class)
        if _class_list_strings:
            information[_class] = {}
            for list_string in _class_list_strings:
                split_string = list_string.split()
                information[_class].update({split_string[1].capitalize(): split_string[0][:-1]})
        else:
            information[_class] = f"'{_class}' class doesn't exist"
    return information

async def run(telephone_number, default = []):
    if telephone_number == 'test':
        html = await get_html(telephone_number, 'test')
        parsed_html = parse_html(html)
        return get_information(parsed_html)
    elif default is  run.__defaults__[0]:
        html = await get_html(telephone_number)
        print(html)
        parsed_html = parse_html(html)
        return get_information(parsed_html)
    else:
        html = await get_html(telephone_number)
        parsed_html = parse_html(html)
        classes = get_classes()
        return get_information(parsed_html, classes)