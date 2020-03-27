import library
import asyncio
from library import Server, Client
import aiohttp
from aiohttp import web
import json


async def get_one(request):
    telephone_number = request.query['number']
    response_dict = await  library.run(telephone_number)
    return web.json_response(response_dict)

async def post_one(request):
    telephone_number = await request.text()
    response_dict = await library.run(telephone_number)
    return web.json_response(response_dict)

async def post_many(request):
    number_json = await request.json()
    response_dict = {}
    for number in number_json.get('number'):
        number_information = await library.run(number)
        response_dict[f'{number}'] = number_information
    return web.json_response(response_dict)

app = web.Application()
app.add_routes([web.get('/one', get_one),
                web.post('/one', post_one),
                web.post('/many', post_many)])
web.run_app(app)