import sys
import requests
import re
import csv
from bs4 import BeautifulSoup


def get_products(url):
    page = get_page(url)
    site = get_site_from_url(url)
    found_products = []
    print(f'name;price;stars;reviews_count')
    while len(found_products) <= 2000:
        products = parse_page(page)
        found_products.extend(products)
        next_url = get_next_page_url(page, site)
        if next_url:
            page_number = get_page_number_from_url(next_url)
            print(f'page: {page_number}')
            page = get_page(next_url)
        else:
            print('no more pages found')
            break

    print(f'total products found: {len(found_products)}')

    return found_products


def save_results(data, filename='matite.csv'):
    fieldnames = ['name', 'price', 'stars', 'reviews_count']
    with open(filename, 'w', newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'}
    # response = requests.get(url, headers=headers, verify=False,) #verify = False usato a scuola per evitare problemi con certificato di Zscaler
    response = requests.get(url, headers=headers)

    page = None
    print(f'status_code: {response.status_code}')
    if response.status_code == 200:
        if "matite colorate" in response.text:  # controlliamo che stiamo analizzando la pagina giusta
            page = response.text
    else:
        print('error loading page content', file=sys.stderr)

    return page


def get_page_number_from_url(url):
    pattern = r"page=(?P<page>\d+)"
    match = re.search(pattern, url)
    page = None
    if match:
        page = match.group('page')

    return page


def get_site_from_url(url):
    pattern = r'(?P<site>(?P<protocol>http[s]?)://(?P<domain>[\w\.]+))'
    match = re.search(pattern, url)
    site = ''
    if match:
        site = match.group('site')

    return site


def get_next_page_url(page, site=None):
    next_url = None
    # specify the parser type or BS will auto find a possible parser
    soup = BeautifulSoup(page, 'html.parser')
    next_page_button = soup.find('a', class_='s-pagination-next')
    # print(next_page_button)
    if next_page_button:
        next_url = next_page_button['href']
        if 'http' not in next_url:
            next_url = site + next_url
    return next_url


def parse_page(page):
    # ora bisogna esaminare ogni singolo prodotto estraendo i dati necessari
    # specify the parser type or BS will auto find a possible parser
    soup = BeautifulSoup(page, 'html.parser')
    # detail = soup.find('div', class_="productDetail")
    # cards = lista di elementi corrispondenti alla ricerca fatta da "find_all"
    cards = soup.find_all('div', class_="s-card-container")
    products_quantity = len(cards)
    print(f'products in page: {products_quantity}')

    products = []
    for i, card in enumerate(cards):
        product = {}

        name = get_product_name(card)
        price = get_product_price(card)
        stars = get_product_stars(card)
        reviews_count = get_product_reviews_count(card)

        product['name'] = name
        product['price'] = price
        product['stars'] = stars
        product['reviews_count'] = reviews_count

        products.append(product)

        # print(f'{product}')

    return products


def get_product_name(card):
    name = 'NOT FOUND'
    s = card.find('span', class_='a-size-base-plus a-color-base a-text-normal')
    if s:
        name = s.text.encode("ascii", "ignore").decode("utf-8")
    return name


def get_product_price(card):
    price = 'NOT FOUND'
    s = card.find('span', class_="a-price")
    if s:
        pricespan = s.find('span', class_="a-offscreen")
        price_str = pricespan.text
        price_str = price_str.replace(u'\xa0', u' ')
        price = float(price_str.split(' ')[0].replace(',', '.').strip())
    return price


def get_product_stars(card):
    stars = 'NOT FOUND'
    d = card.find('div', class_="a-row a-size-small")
    if d and 'stelle' in d.text:
        stars_str = d.find('span')['aria-label']
        v1 = stars_str.split(' ')[0].replace(',', '.')
        v2 = stars_str.split(' ')[2]
        stars = round(float(v1)/int(v2), 2)

    return stars


def get_product_reviews_count(card):
    rc = 'NOT FOUND'
    d = card.find('div', class_="a-row a-size-small")
    # print(d)
    if d:
        rc = int((d.select('span:nth-of-type(2)')
                 [0]['aria-label']).split(' ')[0].replace('.', ''))
    return rc


def run():
    url = 'https://www.amazon.it/s?k=matite+colorate&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3PR3LR3MURG17&sprefix=matite+colorate%2Caps%2C508&ref=nb_sb_noss_1'
    data = get_products(url)
    save_results(data, 'matite.csv')


if __name__ == '__main__':
    run()
