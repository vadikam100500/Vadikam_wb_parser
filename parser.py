import asyncio
import csv
import time
from typing import List
import aiohttp

from bs4 import BeautifulSoup

from main import se

file = 'things.csv'
url_main = 'https://www.wildberries.ru'
# final list with all information
elements: List = []


def parser_main(url):
    # we need this list, to stop parcing if pagination
    page = [0, 1]
    while page[-1] != page[-2]:
        need_page = page[-1]
        # connect to each page in pagination
        final_url = f'{url}?page={need_page}'
        print(
            f'Идет парсинг каждого товара на странице №{need_page}, подождите'
        )
        # get list with href for each item
        item_urls = items_urls(final_url)
        # put new nuber of next page or stop parcing
        if item_urls:
            page.append(need_page + 1)
        else:
            page.append(need_page)
        asyncio.run(get_data(item_urls))
    print(f"Получено {len(elements)} товаров")
    save_file(elements, file)
    print(f"Товары сохранены в файл {file}")


def items_urls(url):
    # i think its clear
    resp = se.get(url)
    need_page = BeautifulSoup(resp.content, 'html.parser')
    items = need_page.find_all(
        'a', class_='product-card__main j-open-full-product-card'
    )
    item_urls = []
    for item in items:
        href = item.get('href')
        item_url = f'{url_main}{href}'
        item_urls.append(item_url)
    return item_urls


async def get_data(item_urls):
    tasks = []
    for item_url in item_urls:
        task = asyncio.create_task(parser_part(item_url))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def parser_part(item_url):
    # i think its also clear
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/91.0.4472.114"
            "Safari/537.36"
        ),
        "accept-encoding": "gzip, deflate, br",
        "accept": "*/*",
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url=item_url, headers=headers)
        item_cart = BeautifulSoup(await resp.text(), "html.parser")
        header = item_cart.find_all('h1')
        for part in header:
            brand = part.find('span').get_text()
        price = item_cart.find_all('p', class_="price-block__price-wrap")
        for part in price:
            try:
                old_price = part.find(
                    'del', class_="price-block__old-price j-final-saving"
                ).get_text().replace(u'\xa0', '')
            except AttributeError:
                old_price = '-'
            try:
                new_price = part.find(
                    'span', class_="price-block__final-price"
                ).get_text(strip=True).replace(u'\xa0', '')
            except AttributeError:
                new_price = '-'
            try:
                discount = (
                    int(new_price.replace(u'₽', '')) /
                    int(old_price.replace(u'₽', ''))
                )*100
            except ValueError:
                discount = 0
        about = item_cart.find_all(
            'div', class_="collapsable__content j-description"
        )
        for part in about:
            try:
                discription = (
                    part.find('p', class_="collapsable__text").get_text()
                )
            except AttributeError:
                discription = 'Описание отсутствует'
        elements.append({
            "Брэнд": brand,
            "Описание": discription,
            "Ссылка": item_url,
            "Цена без скидки": old_price,
            "Цена со скидкой": new_price,
            "Скидка в процентах": '%.1f' % discount,
        })


def save_file(items, path):
    # and here
    with open(path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Брэнд", "Описание", "Ссылка",
            "Цена без скидки", "Цена со скидкой", "Скидка в процентах"
        ])
        for item in items:
            writer.writerow([
                item["Брэнд"], item["Описание"],
                item["Ссылка"], item["Цена без скидки"],
                item["Цена со скидкой"], item["Скидка в процентах"]
            ])
