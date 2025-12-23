# -*- coding: utf-8 -*-
"""
Translate selected fields in JSON datasets from Russian to Uzbek.
- Fields translated: type, genre, country (per value, comma-separated parts are mapped individually)
- collections.json: translate collection names (2nd element of each [id, name] pair)
- Preserves: name/title, ids, years, poster URLs, ratings, quality, etc.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TYPE_MAP = {
    "Фильмы": "Filmlar",
    "Сериалы": "Seriallar",
    "Мультфильмы": "Multfilmlar",
    "Мультсериалы": "Multseriallar",
    "Аниме-фильмы": "Anime filmlar",
    "Аниме-сериалы": "Anime seriallar",
    "ТВ-Шоу": "TV-shou",
}

GENRE_MAP = {
    "Комедия": "Komediya",
    "Боевик": "Jangari",
    "Приключения": "Sarguzasht",
    "Фантастика": "Fantastika",
    "Фэнтези": "Fentezi",
    "Ужасы": "Qo‘rqinchli",
    "Триллер": "Triller",
    "Драма": "Drama",
    "Мелодрама": "Melodrama",
    "Детектив": "Detektiv",
    "Криминал": "Jinoyat",
    "Военный": "Harbiy",
    "Исторический": "Tarixiy",
    "Документальный": "Hujjatli",
    "Биографический": "Biografik",
    "Мюзикл": "Myuzikl",
    "Семейный": "Oilaviy",
    "Короткометражный": "Qisqa metrajli",
    "Спортивный": "Sport",
    "Музыка": "Musiqa",
    "Вестерн": "Vesten",
    "Психологический": "Psixologik",
    "Зарубежный": "Xorijiy",
    "Реальное ТВ": "Realiti-shou",
    "Трейлер": "Treyler",
    "Ток-шоу": "Tok-shou",
    "Путешествия": "Sayohat",
    "Развлекательный": "Ko‘ngilochar",
    "Детский": "Bolalar",
}

COUNTRY_MAP = {
    "США": "AQSH",
    "Россия": "Rossiya",
    "Великобритания": "Buyuk Britaniya",
    "Япония": "Yaponiya",
    "Германия": "Germaniya",
    "Франция": "Fransiya",
    "Италия": "Italiya",
    "Испания": "Ispaniya",
    "Канада": "Kanada",
    "Китай": "Xitoy",
    "Ирландия": "Irlandiya",
    "Бельгия": "Belgiya",
    "Люксембург": "Lyuksemburg",
    "Дания": "Daniya",
    "ЮАР": "JAR",
    "Мексика": "Meksika",
    "Перу": "Peru",
    "Нидерланды": "Niderlandiya",
    "Норвегия": "Norvegiya",
    "Австрия": "Avstriya",
    "Финляндия": "Finlyandiya",
    "Эстония": "Estoniya",
    "Корея Южная": "Janubiy Koreya",
    "Гонконг": "Gonkong",
    "Швеция": "Shvetsiya",
    "Португалия": "Portugaliya",
    "Турция": "Turkiya",
    "Чехия": "Chexiya",
    "Словакия": "Slovakiya",
    "Пакистан": "Pokiston",
    "Филиппины": "Filippin",
    "Нигерия": "Nigeriya",
    "Индия": "Hindiston",
    "Казахстан": "Qozog'iston",
    "Польша": "Polsha",
}

COLLECTIONS_MAP = {
    "Рождественские": "Rojdestvo filmlari",
    "Ситкомы": "Sitkomlar",
    "С наградами": "Mukofotli",
    "Фильмы-катастрофы": "Falokat filmlari",
    "Для женщин": "Ayollar uchun",
    "Для мужчин": "Erkaklar uchun",
    "С неожиданным концом": "Kutilmagan yakunli",
    "Для взрослых": "Kattalar uchun",
    "Про боевые искусства": "Jang san'ati haqida",
    "Про вампиров": "Vampirlar haqida",
    "Про животных": "Hayvonlar haqida",
    "Про ограбления, аферы и мошенников": "O‘g‘irlik, firibgarlik va qaroqchilar haqida",
    "Для молодёжи": "Yoshlar uchun",
    "Про призраков": "Ruhlar haqida",
    "Про маньяков": "Manyaklar haqida",
    "Про монстров": "Monsterlar haqida",
    "Про жизнь": "Hayot haqida",
    "Про космос": "Koinot haqida",
    "Психологические": "Psixologik",
    "Экранизация книг": "Kitob ekranizatsiyalari",
    "Мотивирующие": "Motivatsion",
    "Самые кассовые": "Eng kassabop",
    "Романтические комедии": "Romantik komediyalar",
    "Про любовь": "Muhabbat haqida",
    "На реальных событиях": "Haqiqiy voqealarga asoslangan",
    "Про супергероев": "Superqahramonlar haqida",
    "Про подростков": "O‘smirlar haqida",
    "Фильмы на Хэллоуин": "Helouin filmlari",
    "Советские": "Sovet",
    "Про агентов": "Agentlar haqida",
    "Про зомби": "Zombilar haqida",
    "Про оборотней": "Oborotenlar haqida",
    "Про тюрьму": "Habsxona haqida",
    "Про мафию, банды": "Mafiya va to‘dalar haqida",
    "Про ведьм": "Jodugarlar haqida",
    "Про полицию": "Politsiya haqida",
    "Антиутопии": "Antiutopiyalar",
    "Про роботов": "Robotlar haqida",
    "Про войну 1939-1945": "1939–1945 urushi haqida",
    "Про инопланетян": "Begona sayyoraliklar haqida",
    "Про путешествия": "Sayohat haqida",
    "Про девушек": "Qizlar haqida",
    "Про школу": "Maktab haqida",
    "Про футбол": "Futbol haqida",
    "Про спорт": "Sport haqida",
    "Лучшие фильмы 20 века": "20-asrning eng yaxshi filmlari",
    "Биографии": "Biografiyalar",
    "Про детей": "Bolalar haqida",
    "Про акул": "Akulalar haqida",
    "Про звезд": "Yulduzlar haqida",
    "Молодежные комедии": "Yoshlar komediyalari",
    "Про танки": "Tanklar haqida",
    "Про снайперов": "Snayperlar haqida",
    "Про острова": "Orollar haqida",
    "Про динозавров": "Dinozavrlar haqida",
    "Про бывших": "Sobiq sevgililar haqida",
    "Про средневековье": "O‘rta asrlar haqida",
    "Про гонки": "Poygalar haqida",
    "Про апокалипсис": "Apokalipsis haqida",
    "Про путешествия во времени": "Vaqt sayohati haqida",
    "Про драконов": "Ajdarlar haqida",
    "Про докторов": "Shifokorlar haqida",
    "Музыкальные": "Musiqiy",
    "Про баскетбол": "Basketbol haqida",
    "Кулинария": "Oshpazlik",
    "Про Чернобыльскую катастрофу": "Chernobil falokati haqida",
    "Лауреат премии \"Оскар\"": "Oskar mukofoti sohiblari",
}

FILES = [
    'news_films.json','news_serials.json','news_show.json',
    'popular_anime.json','popular_anime_serials.json','popular_cartoon.json',
    'popular_cartoon_serials.json','popular_films.json','popular_series.json','popular_show.json',
]


def map_csv(text: str, mapping: dict) -> str:
    parts = [s.strip() for s in text.split(',')]
    return ', '.join(mapping.get(s, s) for s in parts)


def process_data_files():
    for fname in FILES:
        p = ROOT / fname
        data = json.loads(p.read_text(encoding='utf-8'))
        changed = 0
        for item in data.get('data', []):
            if not isinstance(item, dict):
                continue
            v = item.get('type')
            if isinstance(v, str):
                nv = TYPE_MAP.get(v, v)
                if nv != v:
                    item['type'] = nv; changed += 1
            v = item.get('country')
            if isinstance(v, str) and v:
                nv = map_csv(v, COUNTRY_MAP)
                if nv != v:
                    item['country'] = nv; changed += 1
            v = item.get('genre')
            if isinstance(v, str) and v:
                nv = map_csv(v, GENRE_MAP)
                if nv != v:
                    item['genre'] = nv; changed += 1
        p.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding='utf-8')
        print(f"{fname}: changed {changed}")


def process_collections():
    p = ROOT / 'collections.json'
    coll = json.loads(p.read_text(encoding='utf-8'))
    changed = 0
    rows = []
    for row in coll.get('data', []):
        if isinstance(row, list) and len(row) == 2 and isinstance(row[1], str):
            name = row[1]
            nv = COLLECTIONS_MAP.get(name, name)
            if nv != name:
                changed += 1
            rows.append([row[0], nv])
        else:
            rows.append(row)
    coll['data'] = rows
    p.write_text(json.dumps(coll, ensure_ascii=False, indent=4), encoding='utf-8')
    print(f"collections.json: changed {changed}")


if __name__ == '__main__':
    process_data_files()
    process_collections()
