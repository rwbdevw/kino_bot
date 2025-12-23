 # -*- coding: utf-8 -*-
from datetime import timedelta, date

import requests
import asyncio
import aiohttp
import re
import sqlite3
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from datetime import date

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from keyboards import *
from config import *
from pagination import InlinePagination, InlinePagination2, FavoritesPagination, NewsPagination
from db import Sqliter


bot = Bot(token=TOKEN, parse_mode='HTML')
admin_id = admins
chatid = chat
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
db = Sqliter('database.db')

category_list = {'films': 'Filmlar', 'serials' : 'Seriallar','series' : 'Seriallar', 'cartoons':'Multfilmlar', 'cartoon':'Multfilmlar', 'cartoon-serials' : 'Multseriallar', 'cartoon-series': 'Multseriallar', 'anime-film': 'Anime filmlar', 'anime' : 'Anime filmlar', 'anime-serials' : 'Anime seriallar', 'anime-series' : 'Anime seriallar', 'tv-shows' : 'TV-shou', 'tv-show': 'TV-shou', 'film': 'Filmlar'}
last_domain = ''

class GetUserInfo(StatesGroup):
    us_zapros_video = State()
    us_zapros_film = State()
    us_zapros_serial = State()
    us_zapros_animefilm = State()
    us_zapros_animeser = State()
    us_zapros_cartoon = State()
    us_zapros_cartoonser = State()
    us_zapros_tv = State()
    us_zapros_film_number = State()
    us_zapros_serial_number = State()
    us_zapros_animefilm_number = State()
    us_zapros_animeser_number = State()
    us_zapros_cartoon_number = State()
    us_zapros_cartoonser_number = State()
    us_zapros_tv_number = State()

print("KO‘PROQ BOTLAR CONFF.ORG DA")
database = open("users_id.txt", "r", encoding="utf-8")
datausers = set()
for line in database:
    datausers.add(line.strip())
database.close()

async def add_collection(data):
    with open('collections.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_news_films(data):
    with open('news_films.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_news_serials(data):
    with open('news_serials.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_news_show(data):
    with open('news_show.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_popular_films(data):
    with open('popular_films.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_popular_series(data):
    with open('popular_series.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_popular_cartoon(data):
    with open('popular_cartoon.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_popular_cartoon_serials(data):
    with open('popular_cartoon_serials.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_popular_anime(data):
    with open('popular_anime.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_popular_anime_serials(data):
    with open('popular_anime_serials.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def add_popular_show(data):
    with open('popular_show.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def update_popular():
    print('update_popular | Yangi mashhur filmlarni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi mashhur filmlar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1673051707.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e&sort=-views&type=films&limit=50&year=2023', timeout=None) as response:
            response = await response.json()
    popular_films = []
    results = response['results']
    for result in results:
        film_id = result['id']
        name = result['name']
        type = category_list[result['type']]
        year = result["year"]
        poster = result["poster"]
        try:
            kinopoisk = result["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = result["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = result["quality"]
        except KeyError:
            quality = None
        try:
            country = result["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        try:
            genre = result['genre'].values()
            genre = ', '.join(genre)
        except KeyError:
            genre = ''
        popular_films.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'kinopoisk': kinopoisk, 'imdb': imdb})
    data = {'data': popular_films}
    await add_popular_films(data)
    print('update_popular | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{date.today()}</b> | <b>«Mashhur»</b> bo‘limining filmlar qismi muvaffaqiyatli yangilandi.\n🏅 Mashhur <b>filmlar</b> yangilandi va qo‘shildi.\n\n👉 @kinozzz_new_bot')

async def update_popular_mult():
    print('update_popular | Yangi mashhur multfilmlarni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi mashhur multfilmlar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1673051707.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e&sort=-views&type=cartoon&limit=50&year=2023', timeout=None) as response:
            response = await response.json()
    popular_cartoon = []
    results = response['results']
    for result in results:
        film_id = result['id']
        name = result['name']
        type = category_list[result['type']]
        year = result["year"]
        poster = result["poster"]
        try:
            kinopoisk = result["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = result["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = result["quality"]
        except KeyError:
            quality = None
        try:
            country = result["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        try:
            genre = result['genre'].values()
            genre = ', '.join(genre)
        except KeyError:
            genre = ''
        popular_cartoon.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'kinopoisk': kinopoisk, 'imdb': imdb})
    data = {'data': popular_cartoon}
    await add_popular_cartoon(data)
    print('update_popular | Yangi mashhur multseriallarni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi mashhur multseriallar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1673051707.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e&sort=-views&type=cartoon-serials&join_seasons=false&limit=50&year=2023', timeout=None) as response:
            response = await response.json()
    popular_cartoon_serials = []
    results = response['results']
    for result in results:
        film_id = result['id']
        name = result['name']
        type = category_list[result['type']]
        year = result["year"]
        poster = result["poster"]
        try:
            kinopoisk = result["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = result["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = result["quality"]
        except KeyError:
            quality = None
        try:
            country = result["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        try:
            genre = result['genre'].values()
            genre = ', '.join(genre)
        except KeyError:
            genre = ''
        popular_cartoon_serials.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'kinopoisk': kinopoisk, 'imdb': imdb})
    data = {'data': popular_cartoon_serials}
    current_date = date.today()
    await add_popular_cartoon_serials(data)
    print('update_popular | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{current_date}</b> | <b>«Mashhur»</b> bo‘limining multfilmlar qismi muvaffaqiyatli yangilandi.\n🏅 Mashhur <b>multfilmlar</b> va <b>multseriallar</b> yangilandi va qo‘shildi.\n\n👉 @kinozzz_new_bot')

async def update_popular_anime():
    print('update_popular | Yangi mashhur anime-larni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi mashhur anime-lar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1673051707.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e&sort=-views&type=anime&limit=50&year=2023', timeout=None) as response:
            response = await response.json()
    popular_anime = []
    results = response['results']
    for result in results:
        film_id = result['id']
        name = result['name']
        type = category_list[result['type']]
        year = result["year"]
        poster = result["poster"]
        try:
            kinopoisk = result["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = result["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = result["quality"]
        except KeyError:
            quality = None
        try:
            country = result["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        try:
            genre = result['genre'].values()
            genre = ', '.join(genre)
        except KeyError:
            genre = ''
        popular_anime.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'kinopoisk': kinopoisk, 'imdb': imdb})
    data = {'data': popular_anime}
    await add_popular_anime(data)
    print('update_popular | Yangi mashhur anime-seriallarni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi mashhur anime-seriallar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1673051707.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e&sort=-views&type=anime-serials&join_seasons=false&limit=50&year=2023', timeout=None) as response:
            response = await response.json()
    popular_anime_serials = []
    results = response['results']
    for result in results:
        film_id = result['id']
        name = result['name']
        type = category_list[result['type']]
        year = result["year"]
        poster = result["poster"]
        try:
            kinopoisk = result["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = result["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = result["quality"]
        except KeyError:
            quality = None
        try:
            country = result["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        try:
            genre = result['genre'].values()
            genre = ', '.join(genre)
        except KeyError:
            genre = ''
        popular_anime_serials.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'kinopoisk': kinopoisk, 'imdb': imdb})
    data = {'data': popular_anime_serials}
    current_date = date.today()
    await add_popular_anime_serials(data)
    print('update_popular | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{current_date}</b> | <b>«Mashhur»</b> bo‘limining anime qismi muvaffaqiyatli yangilandi.\n🏅 Mashhur <b>anime filmlar</b> va <b>anime seriallar</b> yangilandi va qo‘shildi.\n\n👉 @kinozzz_new_bot')

async def update_popular_show():
    print('update_popular | Yangi mashhur TV-shoularni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi mashhur TV-shoular mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1673051707.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e&sort=-views&type=show&limit=50&year=2023', timeout=None) as response:
            response = await response.json()
    popular_show = []
    results = response['results']
    for result in results:
        film_id = result['id']
        name = result['name']
        type = category_list[result['type']]
        year = result["year"]
        poster = result["poster"]
        try:
            kinopoisk = result["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = result["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = result["quality"]
        except KeyError:
            quality = None
        try:
            country = result["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        try:
            genre = result['genre'].values()
            genre = ', '.join(genre)
        except KeyError:
            genre = ''
        popular_show.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'imdb': imdb, 'kinopoisk': kinopoisk})
    data = {'data': popular_show}
    current_date = date.today()
    await add_popular_show(data)
    print('update_popular | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{current_date}</b> | <b>«Mashhur»</b> bo‘limining TV-shou qismi muvaffaqiyatli yangilandi.\n🏅 Mashhur <b>TV-shoular</b> yangilandi va qo‘shildi.\n\n👉 @kinozzz_new_bot')

async def update_domain():
    global last_domain
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1665331096.bhcesh.me/embed-domain?token=3794a7638b5863cc60d7b2b9274fa32e') as response:
            response = await response.json()
    domain = response["domain"]
    if domain != last_domain:
        db.update_domain(domain)
        last_domain = domain

async def update_news_films():
    print('update_news_films | Yangi filmlarni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi filmlar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1664409738.bhcesh.me/video/news?limit=50&type=films&token=3794a7638b5863cc60d7b2b9274fa32e&year=2023', timeout=None) as response:
            response = await response.json()
    results = response['results']
    print(len(results))
    results = [result1['id'] for result1 in results]
    results = list(set(results))
    print(len(results))
    news_films = []
    for result in results:
        film_id = result
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api1663355922.bhcesh.me/franchise/details?token=3794a7638b5863cc60d7b2b9274fa32e&id={film_id}', timeout=None) as response:
                film_data = await response.json()
        name = film_data['name']
        type = category_list[film_data['type']]
        year = film_data["year"]
        poster = film_data["poster"]
        try:
            kinopoisk = film_data["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = film_data["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = film_data["quality"]
        except KeyError:
            quality = None
        try:
            country = film_data["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        print(name)
        try:
            genre = film_data['genre'].values()
            genre = ', '.join(genre)
        except:
            genre = ''
        news_films.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'imdb': imdb, 'kinopoisk': kinopoisk})
        await asyncio.sleep(3)
    news_films = {'data': news_films}
    current_date = date.today()
    await add_news_films(news_films)
    print('update_news_films | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{current_date}</b> | <b>«Yangiliklar»</b> bo‘limining filmlar qismi muvaffaqiyatli yangilandi.\n🆕 Yangi <b>filmlar</b> qo‘shildi.\n\n👉 @kinozzz_new_bot')

async def update_news_serials():
    print('update_news_serials | Yangi seriallarni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi seriallar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1664409738.bhcesh.me/video/news?limit=50&join_seasons=false&type=serials&token=3794a7638b5863cc60d7b2b9274fa32e&year=2023', timeout=None) as response:
            response = await response.json()
    results = response['results']
    print(len(results))
    results = [result1['id'] for result1 in results]
    results = list(set(results))
    print(len(results))
    news_serials = []
    for result in results:
        film_id = result
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api1663355922.bhcesh.me/franchise/details?token=3794a7638b5863cc60d7b2b9274fa32e&id={film_id}&join_seasons=false', timeout=None) as response:
                film_data = await response.json()
        name = film_data['name']
        type = category_list[film_data['type']]
        year = film_data["year"]
        poster = film_data["poster"]
        try:
            kinopoisk = film_data["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = film_data["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = film_data["quality"]
        except KeyError:
            quality = None
        try:
            country = film_data["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        print(name)
        try:
            genre = film_data['genre'].values()
            genre = ', '.join(genre)
        except:
            genre = ''
        news_serials.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'imdb': imdb, 'kinopoisk': kinopoisk})
        await asyncio.sleep(3)
    news_serials = {'data': news_serials}
    current_date = date.today()
    await add_news_serials(news_serials)
    print('update_news_serials | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{current_date}</b> | <b>«Yangiliklar»</b> bo‘limining seriallar qismi muvaffaqiyatli yangilandi.\n🆕 Yangi <b>seriallar</b> qo‘shildi.\n\n👉 @kinozzz_new_bot')

async def update_news_show():
    print('update_news_cartoon | Yangi TV-shoularni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi TV-shoular mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1664409738.bhcesh.me/video/news?limit=300&type=show&token=3794a7638b5863cc60d7b2b9274fa32e&year=2023', timeout=None) as response:
            response = await response.json()
    results = response['results']
    print(len(results))
    results = [result1['id'] for result1 in results]
    results = list(set(results))
    print(len(results))
    news_show = []
    for result in results:
        film_id = result
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api1663355922.bhcesh.me/franchise/details?token=3794a7638b5863cc60d7b2b9274fa32e&id={film_id}&join_seasons=false', timeout=None) as response:
                film_data = await response.json()
        name = film_data['name']
        type = category_list[film_data['type']]
        year = film_data["year"]
        poster = film_data["poster"]
        try:
            kinopoisk = film_data["kinopoisk"]
        except KeyError:
            kinopoisk = None
        try:
            imdb = film_data["imdb"]
        except KeyError:
            imdb = None
        try:
            quality = film_data["quality"]
        except KeyError:
            quality = None
        try:
            country = film_data["country"].values()
            country = ', '.join(country)
        except:
            country = ''
        print(name)
        try:
            genre = film_data['genre'].values()
            genre = ', '.join(genre)
        except:
            genre = ''
        news_show.append({'id':film_id, 'name': name, 'year': year,'quality':quality,'genre':genre, 'type':type,'country':country,'poster':poster, 'imdb': imdb, 'kinopoisk': kinopoisk})
        await asyncio.sleep(3)
    news_show = {'data': news_show}
    current_date = date.today()
    await add_news_show(news_show)
    print('update_news_show | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{current_date}</b> | <b>«Yangiliklar»</b> bo‘limining TV-shou qismi muvaffaqiyatli yangilandi.\n🆕 Yangi <b>TV-shoular</b> qo‘shildi.\n\n👉 @kinozzz_new_bot')

async def update_collections():
    print('update_collections | Yangi to‘plamlarni tekshirishni boshladim.')
    await bot.send_message(chat_id=admin_id, text='🔃 Yangi to‘plamlar mavjudligini tekshirish boshlandi.\n🕘 Iltimos, kuting..')
    with open('collections.json', 'r', encoding="utf-8") as f:
        collections = json.load(f)
        collections_data = collections['data']
        collections_data = [(collection_items[0], collection_items[1]) for collection_items in collections_data]
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api1662739038.bhcesh.me/collection?page=1&token=3794a7638b5863cc60d7b2b9274fa32e') as response:
            response = await response.json()
    test_number = response['total'] - (20*round(response['total']/20))
    if test_number < 10 and test_number > 0:
        pages = round(response['total']/20)+1
    else:
        pages = round(response['total']/20)
    for page in range(1, pages+1):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api1662739038.bhcesh.me/collection?page={page}&token=3794a7638b5863cc60d7b2b9274fa32e') as response:
                response = await response.json()
        collection_results = [(collection_items['id'], collection_items['name']) for collection_items in response['results']]
        collections_data = list(set(collections_data + collection_results))
        await asyncio.sleep(3)
    collections['data'] = sorted(collections_data, key=lambda k: k[0], reverse=False)
    current_date = date.today()
    await add_collection(collections)
    print('update_collections | Tekshiruv yakunlandi.')
    await bot.send_message(chat_id=admin_id, text=f'✅ <b>{current_date}</b> | Tekshiruv muvaffaqiyatli yakunlandi.\n🎞️ To‘plamlar yangilandi.')

async def update_collections_films():
    new_films_count = 0
    await bot.send_message(chat_id=admin_id, text='🔃 To‘plamlarda yangi videomateriallar bor-yo‘qligi tekshirilmoqda.\n🕘 Iltimos, kuting..')
    print('update_collections_films | To‘plamlardagi yangi filmlarni tekshirishni boshladim.')

    with open('collections.json', 'r', encoding="utf-8") as f:
        collections = json.load(f)
    for collection_items in collections['data'][41:]:
        collection_id = collection_items[0]
        collections_films = db.get_films(collection_id)
        # print('connect')
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api1662830368.bhcesh.me/list?collection_id={collection_id}&token=3794a7638b5863cc60d7b2b9274fa32e') as response:
                response = await response.json()
        test_number = response['total'] - (500*round(response['total']/500))
        if test_number < 250 and test_number > 0:
            pages = round(response['total']/500)+1
        else:
            pages = round(response['total']/500)
        print(f'Sahifalar soni: {pages}')

        await asyncio.sleep(3)
        for page in range(1,pages+1):
            print(f'To‘plam {collection_id} | Sahifa: {page}')

            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api1662830368.bhcesh.me/list?page={page}&collection_id={collection_id}&limit=500&token=3794a7638b5863cc60d7b2b9274fa32e') as response:
                    response = await response.json()
            try:
                films = response['results']
            except KeyError:
                print(response)
                exit()
            for film in films:
                collection_ids = [film_[1] for film_ in collections_films]
                if str(film['id']) not in collection_ids:
                    new_films_count +=1
                    try:
                        genre = film['genre'].values()
                        genre = ', '.join(genre)
                    except KeyError:
                        genre = ''
                    data = [collection_id, film['id'], film['name'], genre, film["year"], film['iframe_url'], film['poster'], film["type"]]
                    print(data)
                    db.add_film(data)
            await asyncio.sleep(15)
        await asyncio.sleep(15)
    current_date = date.today()
    await bot.send_message(chat_id=chatid, text=f'✅ <b>{current_date}</b> | <b>«To‘plamlar»</b> bo‘limini yangilash muvaffaqiyatli yakunlandi.\n🎬 Qo‘shilgan video soni: <b>{new_films_count}</b>.\n\n👉 @kinozzz_new_bot')
    print('update_collections_films | Parslash yakunlandi.')

async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    file = open('users_id.txt', 'r')
    text = file.read()
    if not str(message.from_user.id) in text:
        all_id = open("users_id.txt", "a", encoding="utf-8")
        all_id.write(str(f"{message.from_user.id}\n"))
        datausers.add(message.from_user.id)
        current_date = date.today()
        db.db_table_val(user_id=message.from_user.id, user_name=message.from_user.username, user_register=current_date)
    text = f'<a href="https://bot.kinozzz.ru/poster/main.png">🎞️</a> <b><u>Kinozzz Bot</u></b> — o‘ziga xos kino-bot bo‘lib, sizga <b>bepul</b> tarzda <b>mahalliy</b> va <b>xorijiy</b> kinoning yangiliklaridan <u>istalgan qurilmadan</u> bahramand bo‘lish imkonini beradi.\n\nKo‘proq botlar CONFF.ORG saytida.'
    await bot.send_message(message.from_user.id, f'{text}', reply_markup=inlinekeyboard)

@dp.callback_query_handler(text="popular_menu", state="*")
async def popular_menu(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/popmenu.png">🚀</a> Siz <b>«Mashhur»</b> bo‘limiga o‘tdingiz, bu yerda joriy yil uchun <b>ommalashgan</b> videomateriallar joylashgan.\n\n<i>👉 Tomosha qilish uchun <b>videomaterial</b> tanlamoqchi bo‘lgan <b>kategoriyani</b> tanlang.</i>', reply_markup=popular_menu_kb)

# Yangiliklar (Filmlar)
@dp.callback_query_handler(text="news_menu", state="*")
async def news_menu(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/news.png">🆕</a> Siz <b>«Yangiliklar»</b> bo‘limiga o‘tdingiz, bu yerda oxirgi sutka ichida <b>qo‘shilgan</b> yangi videomateriallar joylashgan.\n\n<i>👉 Tomosha qilish uchun <b>videomaterial</b> tanlamoqchi bo‘lgan <b>kategoriyani</b> tanlang.</i>', reply_markup=news_menu_kb)

@dp.callback_query_handler(text="news_films", state="*")
async def news_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('news_films.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_films_back_", next_prefix="news_films_next_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("news_films_next_"))
async def next(call: types.CallbackQuery):
    with open('news_films.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('news_films_next_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_films_back_", next_prefix="news_films_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("news_films_back_"))
async def next(call: types.CallbackQuery):
    with open('news_films.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('news_films_back_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_films_back_", next_prefix="news_films_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

# Novinki (Seriyalar)
@dp.callback_query_handler(text="news_serials", state="*")
async def news_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('news_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_serials_back_", next_prefix="news_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("news_serials_next_"))
async def next(call: types.CallbackQuery):
    with open('news_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('news_serials_next_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_serials_back_", next_prefix="news_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("news_serials_back_"))
async def next(call: types.CallbackQuery):
    with open('news_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('news_serials_back_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_serials_back_", next_prefix="news_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

# Novinki (TV-shoular)
@dp.callback_query_handler(text="news_show", state="*")
async def news_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('news_show.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_show_back_", next_prefix="news_show_next_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("news_show_next_"))
async def next(call: types.CallbackQuery):
    with open('news_show.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('news_show_next_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_show_back_", next_prefix="news_show_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Nomi:</b> {name}\n<b>🏅 KinoPoisk:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Mamlakat:</b> {country}\n<b>📀 Sifat:</b> {quality}\n<b>📁 Kategoriya:</b> {type}\n<b>🎦 Janr:</b> {genre}\n<b>🗓️ Yil:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("news_show_back_"))
async def next(call: types.CallbackQuery):
    with open('news_show.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('news_show_back_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="news_show_back_", next_prefix="news_show_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(text="popular_films", state="*")
async def popular_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('popular_films.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_filmsback_", next_prefix="popular_filmsnext_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_filmsnext_"))
async def next(call: types.CallbackQuery):
    with open('popular_films.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_filmsnext_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_filmsback_", next_prefix="popular_filmsnext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_filmsback_"))
async def next(call: types.CallbackQuery):
    with open('popular_films.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_filmsback_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_filmsback_", next_prefix="popular_filmsnext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(text="popular_series", state="*")
async def popular_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('popular_series.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_seriesback_", next_prefix="popular_seriesnext_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_seriesnext_"))
async def next(call: types.CallbackQuery):
    with open('popular_series.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_seriesnext_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_seriesback_", next_prefix="popular_seriesnext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>?? Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_seriesback_"))
async def next(call: types.CallbackQuery):
    with open('popular_series.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_seriesback_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_seriesback_", next_prefix="popular_seriesnext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

# Начало мультфильмов
@dp.callback_query_handler(text="popular_cartoon", state="*")
async def popular_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('popular_cartoon.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_cartoonback_", next_prefix="popular_cartoonnext_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_cartoonnext_"))
async def next(call: types.CallbackQuery):
    with open('popular_cartoon.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_cartoonnext_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_cartoonback_", next_prefix="popular_cartoonnext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_cartoonback_"))
async def next(call: types.CallbackQuery):
    with open('popular_cartoon.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_cartoonback_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_cartoonback_", next_prefix="popular_cartoonnext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

# Начало мультсериалов
@dp.callback_query_handler(text="popular_cartoon_serials", state="*")
async def popular_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('popular_cartoon_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_cartoon_serials_back_", next_prefix="popular_cartoon_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_cartoon_serials_next_"))
async def next(call: types.CallbackQuery):
    with open('popular_cartoon_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_cartoon_serials_next_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_cartoon_serials_back_", next_prefix="popular_cartoon_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_cartoon_serials_back_"))
async def next(call: types.CallbackQuery):
    with open('popular_cartoon_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_cartoon_serials_back_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_cartoon_serials_back_", next_prefix="popular_cartoon_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

# Начало аниме
@dp.callback_query_handler(text="popular_anime", state="*")
async def popular_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('popular_anime.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_animeback_", next_prefix="popular_animenext_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_animenext_"))
async def next(call: types.CallbackQuery):
    with open('popular_anime.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_animenext_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_animeback_", next_prefix="popular_animenext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_animeback_"))
async def next(call: types.CallbackQuery):
    with open('popular_anime.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_animeback_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_animeback_", next_prefix="popular_animenext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

# Начало аниме-сериалов
@dp.callback_query_handler(text="popular_anime_serials", state="*")
async def popular_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('popular_anime_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_anime_serials_back_", next_prefix="popular_anime_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_anime_serials_next_"))
async def next(call: types.CallbackQuery):
    with open('popular_anime_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_anime_serials_next_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_anime_serials_back_", next_prefix="popular_anime_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_anime_serials_back_"))
async def next(call: types.CallbackQuery):
    with open('popular_anime_serials.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_anime_serials_back_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_anime_serials_back_", next_prefix="popular_anime_serials_next_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

# Начало ТВ-шоу
@dp.callback_query_handler(text="popular_show", state="*")
async def popular_menu(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('popular_show.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']

    film_data = popular_films[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_showback_", next_prefix="popular_shownext_")
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_shownext_"))
async def next(call: types.CallbackQuery):
    with open('popular_show.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_shownext_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_showback_", next_prefix="popular_shownext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("popular_showback_"))
async def next(call: types.CallbackQuery):
    with open('popular_show.json', 'r', encoding="utf-8") as f:
        popular_films = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('popular_showback_')[1])-1

    film_data = popular_films[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    imdb = film_data["imdb"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=popular_films, width=2, back_prefix="popular_showback_", next_prefix="popular_shownext_")
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(text="poisk", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/poisk.png">🔍</a> Вы перешли в раздел <b>«Поиск»</b>, пожалуйста, выберите <b>тип поиска</b>, которым желаете воспользоваться.', reply_markup=search)

@dp.callback_query_handler(text="categories", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/search_name.png">🔍</a> Вы перешли в раздел <b>«Поиск по названию»</b>, пожалуйста, выберите <b>категорию</b>, в которой желаете найти <b>видеоматериал</b>.', reply_markup=category)

@dp.callback_query_handler(text="collections")
async def send(call: types.CallbackQuery):
    with open('collections.json', 'r', encoding="utf-8") as f:
        collections = json.load(f)
    pagination = InlinePagination(button_datas=[(collection_items[1], collection_items[0]) for collection_items in collections['data']], width=2)
    kb = pagination.get_page_keyboard(cur_page=1)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/collection.png">🎞️</a> Вы перешли в раздел <b>«Подборки»</b>, пожалуйста, выберите <b>подборку</b>, в которой желаете выбрать <b>видеоматериал</b> для просмотра.', reply_markup=kb)

@dp.callback_query_handler(text="news")
async def send(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    with open('news.json', 'r', encoding="utf-8") as f:
        news = json.load(f)['data']
    film_data = news[0]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    url = film_data["url"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films=news, width=2)
    kb = pagination.get_page_keyboard(cur_page=1, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КиноПоиск:</b> {kinopoisk}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("newsnext_"))
async def next(call: types.CallbackQuery):
    with open('news.json', 'r', encoding="utf-8") as f:
        news = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('newsnext_')[1])-1

    film_data = news[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    url = film_data["url"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films = news, width=2)
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КиноПоиск:</b> {kinopoisk}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("newsback_"))
async def next(call: types.CallbackQuery):
    with open('news.json', 'r', encoding="utf-8") as f:
        news = json.load(f)['data']
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [int(i[0]) for i in favorite_films]
    number_film = int(call.data.split('newsback_')[1])-1

    film_data = news[number_film]
    film_id = film_data['id']
    poster = film_data['poster']
    name = film_data['name']
    year = film_data['year']
    url = film_data["url"]
    country = film_data['country']
    type = film_data['type']
    genre = film_data['genre']
    quality = film_data['quality']
    time = film_data['time']
    kinopoisk = film_data['kinopoisk']

    pagination = NewsPagination(films = news, width=2)
    kb = pagination.get_page_keyboard(cur_page=call.data, fave_status=film_id in favorite_ids)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КиноПоиск:</b> {kinopoisk}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(text="favorites")
async def send(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    # print(favorite_films)
    if len(favorite_films) == 0:
        await call.answer('❗ Вы ещё ничего не добавляли в свои закладки..\n\n🎞️ Добавляйте в закладки любимые видеоматериалы и смотрите их в удобное для Вас время!', show_alert=True)
    else:
        film_id = favorite_films[0][0]
        name = favorite_films[0][2]
        poster = favorite_films[0][6]
        year = favorite_films[0][3]
        genre = favorite_films[0][4]
        url = favorite_films[0][5]
        type = category_list[favorite_films[0][7]]
        pagination = FavoritesPagination(films=favorite_films, width=2)
        kb = pagination.get_page_keyboard(cur_page=1)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("del_favorite|"))
async def next(call: types.CallbackQuery):
    film_id = call.data.split('|')[1]
    # print(film_id)
    favorites = db.get_favorites(call.message.chat.id)
    favorites_ids = [film[0] for film in favorites]
    if str(film_id) in favorites_ids:
        db.del_favorite(film_id)
        await call.answer('❌ Вы удалили данный видеоматериал из своих закладок!', show_alert=True)
    else:
        await call.answer('❗Данный видеоматериал не находится в ваших закладках!', show_alert=True)

@dp.callback_query_handler(lambda c: c.data.startswith("add_favorite|"))
async def next(call: types.CallbackQuery):
    film_id = call.data.split('|')[1]
    favorites = db.get_favorites(call.message.chat.id)
    favorites_ids = [str(film[0]) for film in favorites]
    if film_id not in favorites_ids:
        film_data = db.get_film_by_id(film_id)
        if len(film_data) == 0:
            params = {"id": film_id}
            film_data = requests.get("https://api1663355922.bhcesh.me/franchise/details?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()
            try:
                genre = film_data['genre'].values()
                genre = ', '.join(genre)
            except KeyError:
                genre = ''
            data = [film_id, call.message.chat.id, film_data['name'], film_data['year'], genre, film_data["iframe_url"], film_data['poster'], film_data['type']]
        else:
            film_data = film_data[0]
            data = [film_id, call.message.chat.id, film_data[2], film_data[4], film_data[3], film_data[5], film_data[6], film_data[7]]
        db.add_favorite(data)
        await call.answer('✅ Данный видеоматериал был успешно добавлен в ваши закладки!', show_alert=True)
    else:
        await call.answer('❗ Данный видеоматериал уже находится в ваших закладках!', show_alert=True)

@dp.callback_query_handler(lambda c: c.data.startswith("favenext_"))
async def next(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    number_film = int(call.data.split('favenext_')[1])-1
    pagination = FavoritesPagination(films=favorite_films, width=2)
    kb = pagination.get_page_keyboard(cur_page=call.data)

    film_id = favorite_films[number_film][0]
    name = favorite_films[number_film][2]
    poster = favorite_films[number_film][6]
    year = favorite_films[number_film][3]
    genre = favorite_films[number_film][4]
    url = favorite_films[number_film][5]
    type = favorite_films[number_film][7]
    type = category_list[type]
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("faveback_"))
async def next(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    number_film = int(call.data.split('faveback_')[1])-1
    pagination = FavoritesPagination(films=favorite_films, width=2)
    kb = pagination.get_page_keyboard(cur_page=call.data)

    film_id = favorite_films[number_film][0]
    name = favorite_films[number_film][2]
    poster = favorite_films[number_film][6]
    year = favorite_films[number_film][3]
    genre = favorite_films[number_film][4]
    url = favorite_films[number_film][5]
    type = favorite_films[number_film][7]
    type = category_list[type]
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("item_"))
async def next(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [str(i[0]) for i in favorite_films]
    collection_id = call.data.split('item_')[1]
    collections_films = db.get_films(collection_id)
    collections_films.reverse()
    film_id = str(collections_films[0][1])
    name = collections_films[0][2]
    poster = collections_films[0][6]
    year = collections_films[0][4]
    genre = collections_films[0][3]
    url = collections_films[0][5]
    type = collections_films[0][7]
    type = category_list[type]
    pagination = InlinePagination2(films=collections_films, width=2)

    kb = pagination.get_page_keyboard(cur_page=1, collection_id=collection_id, fave_status=film_id in favorite_ids)

    kb.row(InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="back"))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("n2_"))
async def next(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [str(i[0]) for i in favorite_films]
    collection_id = call.data.split('n2_')[1].split('_')[0]
    number_film = int(call.data.split('n2_')[1].split('_')[1])-1
    collections_films = db.get_films(collection_id)
    collections_films.reverse()
    pagination = InlinePagination2(films = collections_films, width=2)
    film_id = collections_films[number_film][1]
    name = collections_films[number_film][2]
    poster = collections_films[number_film][6]
    year = collections_films[number_film][4]
    genre = collections_films[number_film][3]
    url = collections_films[number_film][5]
    type = collections_films[number_film][7]
    type = category_list[type]
    kb = pagination.get_page_keyboard(cur_page=call.data, collection_id=collection_id, fave_status=film_id in favorite_ids)
    kb.row(InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="back"))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith("b2_"))
async def back_pag(call: types.CallbackQuery):
    favorite_films = db.get_favorites(call.message.chat.id)
    favorite_ids = [i[0] for i in favorite_films]
    collection_id = call.data.split('b2_')[1].split('_')[0]
    number_film = int(call.data.split('b2_')[1].split('_')[1])-1
    collections_films = db.get_films(collection_id)
    collections_films.reverse()
    pagination = InlinePagination2(films = collections_films, width=2)
    film_id = collections_films[number_film][1]
    name = collections_films[number_film][2]
    poster = collections_films[number_film][6]
    year = collections_films[number_film][4]
    genre = collections_films[number_film][3]
    url = collections_films[number_film][5]
    type = collections_films[number_film][7]
    type = category_list[type]
    kb = pagination.get_page_keyboard(cur_page=call.data, collection_id=collection_id, fave_status=film_id in favorite_ids)
    kb.row(InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="back"))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>📁 Категория:</b> {type}\n<b>🎦 Жанр:</b> {genre}\n<b>🗓️ Год:</b> {year}', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("n_"))
async def next(call: types.CallbackQuery):
    with open('collections.json', 'r', encoding="utf-8") as f:
        collections = json.load(f)
    pagination = InlinePagination(button_datas=[(collection_items[1], collection_items[0]) for collection_items in collections['data']], width=2)
    kb = pagination.get_page_keyboard(cur_page=call.data)

    await call.message.edit_reply_markup(reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("b_"))
async def back_pag(call: types.CallbackQuery):
    with open('collections.json', 'r', encoding="utf-8") as f:
        collections = json.load(f)
    pagination = InlinePagination(button_datas=[(collection_items[1], collection_items[0]) for collection_items in collections['data']], width=2)
    kb = pagination.get_page_keyboard(cur_page=call.data)

    await call.message.edit_reply_markup(reply_markup=kb)

@dp.callback_query_handler(text="about", state="*")
async def send(call: types.CallbackQuery):
  await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/about.png">🎞️</a> <b><u>Kinozzz Bot</u></b> — <b>первый онлайн-кинотеатр</b> в Telegram, который предоставляет возможность <b><u>бесплатно</u></b> наслаждаться новинками <b>Российского</b> и <b>зарубежного</b> кинематографа.\n\n💡 <b>Основные возможности бота:</b>\n— Удобный поиск фильмов, сериалов, ТВ-шоу, мультфильмов и т.п. по названию;\n— <b>Подборки</b> видеоматериалов;\n— Функция <b>«Мои закладки»</b>, чтобы любимые фильмы и сериалы были всегда рядом;\n— Удобный плеер;\n— Высокое качество каждого видеоматериала;\n— Ежедневное пополнение новинками кино.', reply_markup=about)

@dp.callback_query_handler(text="contacts", state="*")
async def send(call: types.CallbackQuery):
  await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<b><a href="https://bot.kinozzz.ru/poster/contacts.png">🔥</a> Мы всегда рады новым идеям и предложениям, которые будут полезны для нашей площадки!</b>\n\n📌 <i>В случае возникновения жалоб на авторские права, обращайтесь на e-mail: <b>admin@kinozzz.ru</b></i>', reply_markup=contacts)

@dp.message_handler(commands=['stats'])
async def statistic(message: types.Message):
    if message.from_user.id == admin_id:
        inlinekeyboard_stats = types.InlineKeyboardMarkup()
        inlinekeyboard_stats.add(types.InlineKeyboardButton(text="Общая статистика", callback_data="stat_all"))
        inlinekeyboard_stats.add(types.InlineKeyboardButton(text="Статистика за сутки", callback_data="stat_day"))
        await message.answer('👉 В данном разделе собрана вся статистика бота.\n\nВыберите категорию для просмотра:', reply_markup=inlinekeyboard_stats)

    @dp.callback_query_handler(text="stat_all")
    async def send(call: types.CallbackQuery):
        await call.answer()
        with open('users_id.txt') as myfile:
            count = sum(1 for line in myfile)
        await message.answer(f'👉 Общее количество пользователей бота: <b>{count}</b>')

    @dp.callback_query_handler(text="stat_day")
    async def send(call: types.CallbackQuery):
        await call.answer()
        today = date.today()
        await message.answer(f'👉 Новых пользователей за сутки: <b>{db.get_users_day_reg(today)}</b>')


@dp.message_handler(commands=['all'])
async def send_all(message: types.Message):
    if message.from_user.id == admin_id:
        for user in datausers:
            try:
                await bot.send_message(user, message.text[message.text.find(" "):])
            except:
                print(f'❗[ {user} ] —  нежелательный пользователь.\n\nСоветуем удалить его из базы данных.')
                pass
        await message.answer("✅ Рассылка успешно окончена!\nВсе пользователи бота получили сообщение.")
    else:
        await message.answer('❌ Вы не являетесь администратором данного бота.')

#Поиск по id
@dp.callback_query_handler(text="search_id", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/search_id.png">🆔</a> Пожалуйста, введите и отправьте <b>ID видеоматериала</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте корректный ID, да бы избежать неверную выдачу видеоматериала.</i>', reply_markup=go_poisk)
    await GetUserInfo.us_zapros_video.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_video)
    async def handle_text(message: types.Message, state: FSMContext):
     await state.update_data(us_zapros_video=message.text)
     data = await state.get_data()
     params = {"kinopoisk_id": {data['us_zapros_video']}}
     response = requests.get("https://api1650820663.bhcesh.me/franchise/details?token=3794a7638b5863cc60d7b2b9274fa32e",params=params).json()
     name = response['name']
     film_id = response['id']
     poster = response['poster']
     year = response['year']
     genre = str(response['genre'])
     file_merge = filter(str.isalpha, genre)
     genre2 = "".join(file_merge)
     genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
     try:
        country = response["country"].values()
        country = ', '.join(country)
     except:
        country = ''
        url = response['iframe_url']
     try:
        kinopoisk = response["kinopoisk"]
     except:
         kinopoisk = None
     try:
         imdb = response["imdb"]
     except:
          imdb = None
     try:
         quality = response["quality"]
     except:
         quality = None
     type = response['type']
     favorite_films = db.get_favorites(message.from_user.id)
     favorite_ids = [i[0] for i in favorite_films]
     play = types.InlineKeyboardMarkup()
     play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
     if film_id in favorite_ids:
         play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
     else:
          play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
          play.add(InlineKeyboardButton(text="◀️ Назад", callback_data="poisk"),InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
     await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
     await state.finish()

@dp.callback_query_handler(text="films", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/film.png">🔎</a> Укажите оригинальное название <b>фильма</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте точное название для корректного поиска.</i>', reply_markup=inlinekeyboard2)
    await GetUserInfo.us_zapros_film.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_film)
    async def handle_text(message: types.Message, state: FSMContext):
            await state.update_data(us_zapros_film=message.text)
            data = await state.get_data()
            params = {"type": 'films', "name": {data['us_zapros_film']}}
            response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
            try:
                if str(response).count('activate_time') > 1:
                    resultal = '🔍 В нашей базе нашлось несколько <b>фильмов</b> с подобным названием: \n'
                    count_films = str(response).count('activate_time')
                    for i in range(count_films):
                        resultal += f"\n🔺<b>[ <code>{i}</code> ]</b> {response[i]['name']}"
                        resultal += f" | <b>{response[i]['year']}</b>"
                    resultal += '\n\n✍️ Укажите цифру <b>фильма</b>, который вам нужен.'
                    await message.answer(resultal, reply_markup=inlinekeyboard2)
                    await GetUserInfo.us_zapros_film_number.set()
                    @dp.message_handler(state=GetUserInfo.us_zapros_film_number)
                    async def handle_text(message: types.Message, state: FSMContext):
                        data = await state.get_data()
                        params = {"type": 'films', "name": {data['us_zapros_film']}}
                        response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e",params=params).json()['results']
                        name = response[int(message.text)]['name']
                        film_id = response[int(message.text)]['id']
                        poster = response[int(message.text)]['poster']
                        year = response[int(message.text)]['year']
                        imdb = response[int(message.text)]['imdb']
                        country = response[int(message.text)]['country']
                        type = response[int(message.text)]['type']
                        genre = str(response[int(message.text)]['genre'])
                        file_merge = filter(str.isalpha, genre)
                        genre2 = "".join(file_merge)
                        genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                        try:
                            kinopoisk = response[int(message.text)]["kinopoisk"]
                        except KeyError:
                            kinopoisk = None
                        try:
                            quality = response[int(message.text)]["quality"]
                        except KeyError:
                            quality = None
                        play = types.InlineKeyboardMarkup()
                        play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                        if film_id in favorite_ids:
                            play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                        else:
                            play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                        play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                        InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                        await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                        await state.finish()
                else:
                    name = response[0]['name']
                    poster = response[0]['poster']
                    year = response[0]['year']
                    film_id = response[0]['id']
                    type = response[0]['type']
                    genre = str(response[0]['genre'])
                    file_merge = filter(str.isalpha, genre)
                    genre2 = "".join(file_merge)
                    genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                    try:
                        country = response[0]["country"].values()
                        country = ', '.join(country)
                    except:
                        country = ''
                    url = response[0]['iframe_url']
                    try:
                        kinopoisk = response[0]["kinopoisk"]
                    except KeyError:
                        kinopoisk = None
                    try:
                        imdb = response[0]["imdb"]
                    except KeyError:
                        imdb = None
                    try:
                        quality = response[0]["quality"]
                    except KeyError:
                        quality = None
                    favorite_films = db.get_favorites(message.from_user.id)
                    favorite_ids = [i[0] for i in favorite_films]
                    play = types.InlineKeyboardMarkup()
                    play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                    if film_id in favorite_ids:
                        play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                    else:
                        play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                    play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                    await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                    await state.finish()
            except:
                await message.answer('<a href="https://bot.kinozzz.ru/poster/nosearch.png">😔</a> Не удалось найти <b>фильм</b> с подобным названием.\n\n❗<i>Введите корректное название для более точного поиска.</i>', reply_markup=inlinekeyboard2)
                await state.finish()

@dp.callback_query_handler(text="serials", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/serial.png">🔎</a> Укажите оригинальное название <b>сериала</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте точное название для корректного поиска.</i>', reply_markup=inlinekeyboard3)
    await GetUserInfo.us_zapros_serial.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_serial)
    async def handle_text(message: types.Message, state: FSMContext):
            await state.update_data(us_zapros_serial=message.text)
            data = await state.get_data()
            params = {"type": 'serials', "name": {data['us_zapros_serial']}}
            response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
            try:
                if str(response).count('activate_time') > 1:
                    resultal = '🔍 В нашей базе нашлось несколько <b>сериалов</b> с подобным названием: \n'
                    count_serials = str(response).count('activate_time')
                    for i in range(count_serials):
                        resultal += f"\n🔺<b>[ <code>{i}</code> ]</b> {response[i]['name']}"
                        resultal += f" | <b>{response[i]['year']}</b>"
                    resultal += '\n\n✍️ Укажите цифру <b>сериала</b>, который вам нужен.'
                    await message.answer(resultal, reply_markup=inlinekeyboard3)
                    await GetUserInfo.us_zapros_serial_number.set()
                    @dp.message_handler(state=GetUserInfo.us_zapros_serial_number)
                    async def handle_text(message: types.Message, state: FSMContext):
                        data = await state.get_data()
                        params = {"type": 'serials', "name": {data['us_zapros_serial']}}
                        response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
                        film_id = response[int(message.text)]['id']
                        name = response[int(message.text)]['name']
                        poster = response[int(message.text)]['poster']
                        year = response[int(message.text)]['year']
                        genre = str(response[int(message.text)]['genre'])
                        type = response[int(message.text)]['type']
                        try:
                            country = response[int(message.text)]["country"].values()
                            country = ', '.join(country)
                        except:
                            country = ''
                        genre2 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre)
                        try:
                            kinopoisk = response[int(message.text)]["kinopoisk"]
                        except KeyError:
                            kinopoisk = None
                        try:
                            imdb = response[int(message.text)]["imdb"]
                        except KeyError:
                            imdb = None
                        try:
                            quality = response[int(message.text)]["quality"]
                        except KeyError:
                            quality = None
                        url = response[int(message.text)]['iframe_url']
                        favorite_films = db.get_favorites(message.from_user.id)
                        favorite_ids = [i[0] for i in favorite_films]
                        play = types.InlineKeyboardMarkup()
                        play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                        if film_id in favorite_ids:
                            play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                        else:
                            play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                        play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                        InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                        await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre2}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                        await state.finish()
                else:
                    film_id = response[0]['id']
                    name = response[0]['name']
                    poster = response[0]['poster']
                    year = response[0]['year']
                    type = response[0]['type']
                    try:
                        country = response[0]["country"].values()
                        country = ', '.join(country)
                    except:
                        country = ''
                    genre = str(response[0]['genre'])
                    file_merge = filter(str.isalpha, genre)
                    genre2 = "".join(file_merge)
                    genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                    url = response[0]['iframe_url']
                    try:
                        kinopoisk = response[0]["kinopoisk"]
                    except KeyError:
                        kinopoisk = None
                    try:
                        imdb = response[0]["imdb"]
                    except KeyError:
                        imdb = None
                    try:
                        quality = response[0]["quality"]
                    except KeyError:
                        quality = None
                    favorite_films = db.get_favorites(message.from_user.id)
                    favorite_ids = [i[0] for i in favorite_films]
                    play = types.InlineKeyboardMarkup()
                    play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                    if film_id in favorite_ids:
                        play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                    else:
                        play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                    play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                    await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                    await state.finish()
            except:
                await message.answer('<a href="https://bot.kinozzz.ru/poster/nosearch.png">😔</a> Не удалось найти <b>сериал</b> с подобным названием.\n\n❗<i>Введите корректное название для более точного поиска.</i>', reply_markup=inlinekeyboard3)
                await state.finish()

@dp.callback_query_handler(text="anime_films", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/anime.png">🔎</a> Укажите оригинальное название <b>аниме-фильма</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте точное название для корректного поиска.</i>', reply_markup=inlinekeyboard4)
    await GetUserInfo.us_zapros_animefilm.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_animefilm)
    async def handle_text(message: types.Message, state: FSMContext):
            await state.update_data(us_zapros_animefilm=message.text)
            data = await state.get_data()
            params = {"type": 'anime', "name": {data['us_zapros_animefilm']}}
            response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
            try:
                if str(response).count('activate_time') > 1:
                    resultal = '🔍 В нашей базе нашлось несколько <b>аниме-фильмов</b> с подобным названием: \n'
                    count_anime_films = str(response).count('activate_time')
                    for i in range(count_anime_films):
                        resultal += f"\n🔺<b>[ <code>{i}</code> ]</b> {response[i]['name']}"
                        resultal += f" | <b>{response[i]['year']}</b>"
                    resultal += '\n\n✍️ Укажите цифру <b>аниме-фильма</b>, который вам нужен.'
                    await message.answer(resultal, reply_markup=inlinekeyboard4)
                    await GetUserInfo.us_zapros_animefilm_number.set()
                    @dp.message_handler(state=GetUserInfo.us_zapros_animefilm_number)
                    async def handle_text(message: types.Message, state: FSMContext):
                        data = await state.get_data()
                        params = {"type": 'anime', "name": {data['us_zapros_animefilm']}}
                        response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
                        film_id = response[int(message.text)]['id']
                        name = response[int(message.text)]['name']
                        poster = response[int(message.text)]['poster']
                        try:
                            country = response[int(message.text)]["country"].values()
                            country = ', '.join(country)
                        except:
                            country = ''
                        year = response[int(message.text)]['year']
                        genre = str(response[int(message.text)]['genre'])
                        type = response[int(message.text)]['type']
                        file_merge = filter(str.isalpha, genre)
                        genre2 = "".join(file_merge)
                        genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                        try:
                            kinopoisk = response[int(message.text)]["kinopoisk"]
                        except KeyError:
                            kinopoisk = None
                        try:
                            imdb = response[int(message.text)]["imdb"]
                        except KeyError:
                            imdb = None
                        try:
                            quality = response[int(message.text)]["quality"]
                        except KeyError:
                            quality = None
                        url = response[int(message.text)]['iframe_url']
                        favorite_films = db.get_favorites(message.from_user.id)
                        favorite_ids = [i[0] for i in favorite_films]
                        play = types.InlineKeyboardMarkup()
                        play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                        if film_id in favorite_ids:
                            play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                        else:
                            play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                        play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                        InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                        await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                        await state.finish()
                else:
                    film_id = response[0]['id']
                    name = response[0]['name']
                    poster = response[0]['poster']
                    year = response[0]['year']
                    genre = str(response[0]['genre'])
                    type = response[0]['type']
                    try:
                        country = response[0]["country"].values()
                        country = ', '.join(country)
                    except KeyError:
                        country = ''
                    file_merge = filter(str.isalpha, genre)
                    genre2 = "".join(file_merge)
                    genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                    url = response[0]['iframe_url']
                    try:
                        kinopoisk = response[0]["kinopoisk"]
                    except KeyError:
                        kinopoisk = None
                    try:
                        imdb = response[0]["imdb"]
                    except KeyError:
                        imdb = None
                    try:
                        quality = response[0]["quality"]
                    except KeyError:
                        quality = None
                    favorite_films = db.get_favorites(message.from_user.id)
                    favorite_ids = [i[0] for i in favorite_films]
                    play = types.InlineKeyboardMarkup()
                    play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                    if film_id in favorite_ids:
                        play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                    else:
                        play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                    play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                    await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                    await state.finish()
            except:
                await message.answer('<a href="https://bot.kinozzz.ru/poster/nosearch.png">😔</a> Не удалось найти <b>аниме-фильм</b> с подобным названием.\n\n❗<i>Введите корректное название для более точного поиска.</i>', reply_markup=inlinekeyboard4)
                await state.finish()

@dp.callback_query_handler(text="cartoon_serials", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/mserial.png">🔎</a> Укажите оригинальное название <b>аниме-сериала</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте точное название для корректного поиска.</i>', reply_markup=inlinekeyboard5)
    await GetUserInfo.us_zapros_cartoonser.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_cartoonser)
    async def handle_text(message: types.Message, state: FSMContext):
            await state.update_data(us_zapros_cartoonser=message.text)
            data = await state.get_data()
            params = {"type": 'cartoon-serials', "name": {data['us_zapros_cartoonser']}}
            response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
            try:
                if str(response).count('activate_time') > 1:
                    resultal = '🔍 В нашей базе нашлось несколько <b>мультсериалов</b> с подобным названием: \n'
                    count_cartoon_serials = str(response).count('activate_time')
                    for i in range(count_cartoon_serials):
                        resultal += f"\n🔺<b>[ <code>{i}</code> ]</b> {response[i]['name']}"
                        resultal += f" | <b>{response[i]['year']}</b>"
                    resultal += '\n\n✍️ Укажите цифру <b>мультсериала</b>, который вам нужен.'
                    await message.answer(resultal, reply_markup=inlinekeyboard5)
                    await GetUserInfo.us_zapros_cartoonser_number.set()
                    @dp.message_handler(state=GetUserInfo.us_zapros_cartoonser_number)
                    async def handle_text(message: types.Message, state: FSMContext):
                        data = await state.get_data()
                        params = {"type": 'cartoon-serials', "name": {data['us_zapros_cartoonser']}}
                        response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
                        film_id = response[int(message.text)]['id']
                        name = response[int(message.text)]['name']
                        poster = response[int(message.text)]['poster']
                        try:
                            country = response[int(message.text)]["country"].values()
                            country = ', '.join(country)
                        except:
                            country = ''
                        year = response[int(message.text)]['year']
                        type = response[int(message.text)]['type']
                        genre = str(response[int(message.text)]['genre'])
                        file_merge = filter(str.isalpha, genre)
                        genre2 = "".join(file_merge)
                        genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                        try:
                            kinopoisk = response[int(message.text)]["kinopoisk"]
                        except KeyError:
                            kinopoisk = None
                        try:
                            imdb = response[int(message.text)]["imdb"]
                        except KeyError:
                            imdb = None
                        try:
                            quality = response[int(message.text)]["quality"]
                        except KeyError:
                            quality = None
                        url = response[int(message.text)]['iframe_url']
                        favorite_films = db.get_favorites(message.from_user.id)
                        favorite_ids = [i[0] for i in favorite_films]
                        play = types.InlineKeyboardMarkup()
                        play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                        if film_id in favorite_ids:
                            play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                        else:
                            play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                        play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                        InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                        await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                        await state.finish()
                else:
                    film_id = response[0]['id']
                    name = response[0]['name']
                    poster = response[0]['poster']
                    year = response[0]['year']
                    genre = str(response[0]['genre'])
                    try:
                        country = response[0]["country"].values()
                        country = ', '.join(country)
                    except KeyError:
                        country = ''
                    type = response[0]['type']
                    file_merge = filter(str.isalpha, genre)
                    genre2 = "".join(file_merge)
                    genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                    url = response[0]['iframe_url']
                    try:
                        kinopoisk = response[0]["kinopoisk"]
                    except KeyError:
                        kinopoisk = None
                    try:
                        imdb = response[0]["imdb"]
                    except KeyError:
                        imdb = None
                    try:
                        quality = response[0]["quality"]
                    except KeyError:
                        quality = None
                    favorite_films = db.get_favorites(message.from_user.id)
                    favorite_ids = [i[0] for i in favorite_films]
                    play = types.InlineKeyboardMarkup()
                    play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                    if film_id in favorite_ids:
                        play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                    else:
                        play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                    play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                    await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                    await state.finish()
            except Exception as ex:
                print(ex)
                await message.answer('<a href="https://bot.kinozzz.ru/poster/nosearch.png">😔</a> Не удалось найти <b>мультсериал</b> с подобным названием.\n\n❗<i>Введите корректное название для более точного поиска.</i>', reply_markup=inlinekeyboard5)
                await state.finish()

@dp.callback_query_handler(text="cartoon", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/mfilm.png">🔎</a> Укажите оригинальное название <b>мультфильма</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте точное название для корректного поиска.</i>', reply_markup=inlinekeyboard6)
    await GetUserInfo.us_zapros_cartoon.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_cartoon)
    async def handle_text(message: types.Message, state: FSMContext):
            await state.update_data(us_zapros_cartoon=message.text)
            data = await state.get_data()
            params = {"type": 'cartoon', "name": {data['us_zapros_cartoon']}}
            response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
            try:
                if str(response).count('activate_time') > 1:
                    resultal = '🔍 В нашей базе нашлось несколько <b>мультфильмов</b> с подобным названием: \n'
                    count_cartoon = str(response).count('activate_time')
                    for i in range(count_cartoon):
                        resultal += f"\n🔺<b>[ <code>{i}</code> ]</b> {response[i]['name']}"
                        resultal += f" | <b>{response[i]['year']}</b>"
                    resultal += '\n\n✍️ Укажите цифру <b>мультфильма</b>, который вам нужен.'
                    await message.answer(resultal, reply_markup=inlinekeyboard6)
                    await GetUserInfo.us_zapros_cartoon_number.set()
                    @dp.message_handler(state=GetUserInfo.us_zapros_cartoon_number)
                    async def handle_text(message: types.Message, state: FSMContext):
                        data = await state.get_data()
                        params = {"type": 'cartoon', "name": {data['us_zapros_cartoon']}}
                        response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
                        film_id = response[int(message.text)]['id']
                        name = response[int(message.text)]['name']
                        poster = response[int(message.text)]['poster']
                        try:
                            country = response[int(message.text)]["country"].values()
                            country = ', '.join(country)
                        except KeyError:
                            country = ''
                        type = response[int(message.text)]['type']
                        year = response[int(message.text)]['year']
                        genre = str(response[int(message.text)]['genre'])
                        file_merge = filter(str.isalpha, genre)
                        genre2 = "".join(file_merge)
                        genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                        try:
                            kinopoisk = response[int(message.text)]["kinopoisk"]
                        except KeyError:
                            kinopoisk = None
                        try:
                            imdb = response[int(message.text)]["imdb"]
                        except KeyError:
                            imdb = None
                        try:
                            quality = response[int(message.text)]["quality"]
                        except KeyError:
                            quality = None
                        url = response[int(message.text)]['iframe_url']
                        favorite_films = db.get_favorites(message.from_user.id)
                        favorite_ids = [i[0] for i in favorite_films]
                        play = types.InlineKeyboardMarkup()
                        play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                        if film_id in favorite_ids:
                            play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                        else:
                            play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                        play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                        InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                        await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                        await state.finish()
                else:
                    film_id = response[0]['id']
                    name = response[0]['name']
                    poster = response[0]['poster']
                    year = response[0]['year']
                    genre = str(response[0]['genre'])
                    try:
                        country = response[0]["country"].values()
                        country = ', '.join(country)
                    except KeyError:
                        country = ''
                    type = response[0]['type']
                    file_merge = filter(str.isalpha, genre)
                    genre2 = "".join(file_merge)
                    genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                    url = response[0]['iframe_url']
                    try:
                        kinopoisk = response[0]["kinopoisk"]
                    except KeyError:
                        kinopoisk = None
                    try:
                        imdb = response[0]["imdb"]
                    except KeyError:
                        imdb = None
                    try:
                        quality = response[0]["quality"]
                    except KeyError:
                        quality = None
                    favorite_films = db.get_favorites(message.from_user.id)
                    favorite_ids = [i[0] for i in favorite_films]
                    play = types.InlineKeyboardMarkup()
                    play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                    if film_id in favorite_ids:
                        play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                    else:
                        play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                    play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                    await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                    await state.finish()
            except:
                await message.answer('<a href="https://bot.kinozzz.ru/poster/nosearch.png">😔</a> Не удалось найти <b>мультфильм</b> с подобным названием.\n\n❗<i>Введите корректное название для более точного поиска.</i>', reply_markup=inlinekeyboard6)
                await state.finish()

@dp.callback_query_handler(text="anime_serials", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/anime.png">🔎</a> Укажите оригинальное название <b>аниме-сериала</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте точное название для корректного поиска.</i>', reply_markup=inlinekeyboard7)
    await GetUserInfo.us_zapros_animeser.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_animeser)
    async def handle_text(message: types.Message, state: FSMContext):
            await state.update_data(us_zapros_animeser=message.text)
            data = await state.get_data()
            params = {"type": 'anime-serials', "name": {data['us_zapros_animeser']}}
            response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
            try:
                if str(response).count('activate_time') > 1:
                    resultal = '🔍 В нашей базе нашлось несколько <b>аниме-сериалов</b> с подобным названием: \n'
                    count_anime_serials = str(response).count('activate_time')
                    for i in range(count_anime_serials):
                        resultal += f"\n🔺<b>[ <code>{i}</code> ]</b> {response[i]['name']}"
                        resultal += f" | <b>{response[i]['year']}</b>"
                    resultal += '\n\n✍️ Укажите цифру <b>аниме-сериала</b>, который вам нужен.'
                    await message.answer(resultal, reply_markup=inlinekeyboard7)
                    await GetUserInfo.us_zapros_animeser_number.set()
                    @dp.message_handler(state=GetUserInfo.us_zapros_animeser_number)
                    async def handle_text(message: types.Message, state: FSMContext):
                        data = await state.get_data()
                        params = {"type": 'anime-serials', "name": {data['us_zapros_animeser']}}
                        response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
                        film_id = response[int(message.text)]['id']
                        name = response[int(message.text)]['name']
                        try:
                            country = response[int(message.text)]["country"].values()
                            country = ', '.join(country)
                        except KeyError:
                            country = ''
                        type = response[int(message.text)]['type']
                        poster = response[int(message.text)]['poster']
                        year = response[int(message.text)]['year']
                        genre = str(response[int(message.text)]['genre'])
                        file_merge = filter(str.isalpha, genre)
                        genre2 = "".join(file_merge)
                        genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                        try:
                            kinopoisk = response[int(message.text)]["kinopoisk"]
                        except KeyError:
                            kinopoisk = None
                        try:
                            imdb = response[int(message.text)]["imdb"]
                        except KeyError:
                            imdb = None
                        try:
                            quality = response[int(message.text)]["quality"]
                        except KeyError:
                            quality = None
                        url = response[int(message.text)]['iframe_url']
                        favorite_films = db.get_favorites(message.from_user.id)
                        favorite_ids = [i[0] for i in favorite_films]
                        play = types.InlineKeyboardMarkup()
                        play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                        if film_id in favorite_ids:
                            play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                        else:
                            play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                        play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                        InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                        await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                        await state.finish()
                else:
                    film_id = response[0]['id']
                    name = response[0]['name']
                    poster = response[0]['poster']
                    year = response[0]['year']
                    genre = str(response[0]['genre'])
                    try:
                        country = response[0]["country"].values()
                        country = ', '.join(country)
                    except KeyError:
                        country = ''
                    file_merge = filter(str.isalpha, genre)
                    type = response[0]['type']
                    genre2 = "".join(file_merge)
                    genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                    url = response[0]['iframe_url']
                    try:
                        kinopoisk = response[0]["kinopoisk"]
                    except KeyError:
                        kinopoisk = None
                    try:
                        imdb = response[0]["imdb"]
                    except KeyError:
                        imdb = None
                    try:
                        quality = response[0]["quality"]
                    except KeyError:
                        quality = None
                    favorite_films = db.get_favorites(message.from_user.id)
                    favorite_ids = [i[0] for i in favorite_films]
                    play = types.InlineKeyboardMarkup()
                    play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                    if film_id in favorite_ids:
                        play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                    else:
                        play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                    play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                    await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                    await state.finish()
            except:
                await message.answer('<a href="https://bot.kinozzz.ru/poster/nosearch.png">😔</a> Не удалось найти <b>аниме-сериал</b> с подобным названием.\n\n❗<i>Введите корректное название для более точного поиска.</i>', reply_markup=inlinekeyboard7)
                await state.finish()

@dp.callback_query_handler(text="tv", state="*")
async def send(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '<a href="https://bot.kinozzz.ru/poster/show.png">🔎</a> Укажите оригинальное название <b>ТВ-шоу</b> для поиска.\n\n❗<i><b>Важно:</b> указывайте точное название для корректного поиска.</i>', reply_markup=inlinekeyboard8)
    await GetUserInfo.us_zapros_tv.set()
    await call.answer()
    @dp.message_handler(state=GetUserInfo.us_zapros_tv)
    async def handle_text(message: types.Message, state: FSMContext):
            await state.update_data(us_zapros_tv=message.text)
            data = await state.get_data()
            params = {"type": 'show', "name": {data['us_zapros_tv']}}
            response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
            try:
                if str(response).count('activate_time') > 1:
                    resultal = '🔍 В нашей базе нашлось несколько <b>ТВ-Шоу</b> с подобным названием: \n'
                    count_tv = str(response).count('activate_time')
                    for i in range(count_tv):
                        resultal += f"\n🔺<b>[ <code>{i}</code> ]</b> {response[i]['name']}"
                        resultal += f" | <b>{response[i]['year']}</b>"
                    resultal += '\n\n✍️ Укажите цифру <b>ТВ-Шоу</b>, который вам нужен.'
                    await message.answer(resultal, reply_markup=inlinekeyboard8)
                    await GetUserInfo.us_zapros_tv_number.set()
                    @dp.message_handler(state=GetUserInfo.us_zapros_tv_number)
                    async def handle_text(message: types.Message, state: FSMContext):
                        data = await state.get_data()
                        params = {"type": 'show', "name": {data['us_zapros_tv']}}
                        response = requests.get("https://api1650820663.bhcesh.me/list?token=3794a7638b5863cc60d7b2b9274fa32e", params=params).json()['results']
                        film_id = response[int(message.text)]['id']
                        name = response[int(message.text)]['name']
                        try:
                            country = response[int(message.text)]["country"].values()
                            country = ', '.join(country)
                        except KeyError:
                            country = ''
                        poster = response[int(message.text)]['poster']
                        year = response[int(message.text)]['year']
                        genre = str(response[int(message.text)]['genre'])
                        type = response[int(message.text)]['type']
                        file_merge = filter(str.isalpha, genre)
                        genre2 = "".join(file_merge)
                        genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                        try:
                            kinopoisk = response[int(message.text)]["kinopoisk"]
                        except KeyError:
                            kinopoisk = None
                        try:
                            imdb = response[int(message.text)]["imdb"]
                        except KeyError:
                            imdb = None
                        try:
                            quality = response[int(message.text)]["quality"]
                        except KeyError:
                            quality = None
                        url = response[int(message.text)]['iframe_url']
                        favorite_films = db.get_favorites(message.from_user.id)
                        favorite_ids = [i[0] for i in favorite_films]
                        play = types.InlineKeyboardMarkup()
                        play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                        if film_id in favorite_ids:
                            play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                        else:
                            play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                        play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                        InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                        await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                        await state.finish()
                else:
                    film_id = response[0]['id']
                    name = response[0]['name']
                    poster = response[0]['poster']
                    year = response[0]['year']
                    genre = str(response[0]['genre'])
                    try:
                        country = response[0]["country"].values()
                        country = ', '.join(country)
                    except KeyError:
                        country = ''
                    type = response[0]['type']
                    file_merge = filter(str.isalpha, genre)
                    genre2 = "".join(file_merge)
                    genre3 = re.sub(r"(\w)([А-Я])", r"\1, \2", genre2)
                    url = response[0]['iframe_url']
                    try:
                        kinopoisk = response[0]["kinopoisk"]
                    except KeyError:
                        kinopoisk = None
                    try:
                        imdb = response[0]["imdb"]
                    except KeyError:
                        imdb = None
                    try:
                        quality = response[0]["quality"]
                    except KeyError:
                        quality = None
                    favorite_films = db.get_favorites(message.from_user.id)
                    favorite_ids = [i[0] for i in favorite_films]
                    play = types.InlineKeyboardMarkup()
                    play.add(types.InlineKeyboardButton(text="😍 Смотреть онлайн", url=f'https://bot.kinozzz.ru/play/?id={film_id}'))
                    if film_id in favorite_ids:
                        play.row(InlineKeyboardButton(text="❌ Удалить из закладок", callback_data=f'del_favorite|{film_id}'))
                    else:
                        play.row(InlineKeyboardButton(text="➕ Добавить в закладки", callback_data=f'add_favorite|{film_id}'))
                    play.add(InlineKeyboardButton(text="◀️ Категории", callback_data="categories"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="back"))
                    await bot.send_message(message.from_user.id, f'<b><a href="{poster}">▶️</a> Название:</b> {name}\n<b>🏅 КП:</b> {kinopoisk} | <b>IMDb:</b> {imdb}\n<b>🌍 Страна:</b> {country}\n<b>📀 Качество:</b> {quality}\n<b>📁 Категория: </b> {category_list[type]}\n<b>🎦 Жанр:</b> {genre3}\n<b>🗓️ Год:</b> {year}', reply_markup=play)
                    await state.finish()
            except:
                await message.answer('<a href="https://bot.kinozzz.ru/poster/nosearch.png">😔</a> Не удалось найти <b>ТВ-Шоу</b> с подобным названием.\n\n❗<i>Введите корректное название для более точного поиска.</i>', reply_markup=inlinekeyboard8)
                await state.finish()

@dp.message_handler(content_types=['text'])
async def send_all(message):
  await bot.send_message(message.from_user.id, f'❗К сожалению, ваш запрос не распознан!\n\n<a href="https://bot.kinozzz.ru/poster/error.png">🏠</a> <i>Вернитесь в <b>главное меню</b></i>.', reply_markup=exit)

@dp.callback_query_handler(text="back", state="*")
async def back(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '🏠 Вы вернулись в <b>главное меню</b>.\n\n<a href="https://bot.kinozzz.ru/poster/general.png">🎦</a> Здесь вы можете выбрать <b>раздел</b>, в котором желаете найти или выбрать видеоматериал для просмотра.', reply_markup=inlinekeyboard, inline_message_id=call.inline_message_id)

async def on_startup(dp: Dispatcher):
    print('~~~ Kinozzz Bot успешно запущен! ~~~')
    #await bot.send_message(chat_id=admin_id, text='🚀 <b>Kinozzz Bot</b> успешно запущен!\nОтправьте <b>/start</b> для обновления.')
    # await update_popular_anime()
    # await update_popular_mult()
    # await update_news_films()
    # await update_popular()
    # await update_collections()
    # await update_popular_show()
    scheduler.add_job(update_news_films, 'cron', hour=11, minute=16)
    scheduler.add_job(update_news_serials, 'cron', hour=12, minute=29)
    scheduler.add_job(update_news_show, 'cron', hour=13, minute=18)
    # scheduler.add_job(update_domain, 'interval', minutes=60)
    scheduler.add_job(update_popular, 'cron', hour=1, minute=10)
    scheduler.add_job(update_popular_mult, 'cron', hour=2, minute=30)
    scheduler.add_job(update_popular_anime, 'cron', hour=3, minute=50)
    scheduler.add_job(update_popular_show, 'cron', hour=5, minute=40)
    scheduler.add_job(update_collections_films, 'cron', hour=7, minute=10)
    scheduler.add_job(update_collections, 'cron', hour=23, minute=40)
    scheduler.start()

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


def run_keepalive_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_keepalive_server, daemon=True)
    server_thread.start()
    executor.start_polling(dp, on_startup=on_startup)