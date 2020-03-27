import aiohttp
from aiohttp import web
import json
import asyncio

async def main_get_test(number):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/one', params = {'number': f'{number}'}) as resp:
            with open('json.txt', 'w') as outfile:
                json.dump(await resp.json(), outfile, ensure_ascii= False, indent=4)

async def main_post_test(number):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/one', data = str(number)) as resp:
            with open('json.txt', 'w') as outfile:
                json.dump(await resp.json(), outfile, ensure_ascii= False, indent=4)

async def main_post_many(data = {'number': list(range(84959999999, 84960001000))}):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/many', json = data) as resp:
            with open('json.txt', 'w') as outfile:
                json.dump(await resp.json(), outfile, ensure_ascii= False, indent=4)


asyncio.run(main_post_test(84959999999))