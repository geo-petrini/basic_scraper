import sys
import requests
from bs4 import BeautifulSoup


def get_matite():
    url = 'https://www.galaxus.ch/it/search?q=matite+colorate&is=matite'
    response = requests.get(url)
    print(f'status_code: {response.status_code}')
    if response.status_code == 200:
        if "matite colorate" in response.text:
            print('ok')
        if "Staedtler" in response.text:
            parse_page(response.text)
            #this fails because content in this page is loaded via ajax
    else:
        print('error loading page content', file=sys.stderr)

def get_url(url = 'https://www.galaxus.ch/it/s12/product/staedtler-matite-colorate-multicolore-pastelli-14636759'):
    response = requests.get(url)
    print(f'status_code: {response.status_code}')
    if response.status_code == 200:
        parse_page(response.text)
            #this fails because content in this page is loaded via ajax
    else:
        print('error loading page content', file=sys.stderr)

def run():
    get_matite()
    get_url('https://www.galaxus.ch/it/s12/product/staedtler-matite-colorate-multicolore-pastelli-14636759')

def parse_page(page):
    soup = BeautifulSoup(page, 'html.parser')   #specify the parser type or BS will auto find a possible parser
    detail = soup.find('div', class_="productDetail")
    #print(f'detail: {detail}')
    for e in detail.select('span:nth-child(2) > strong:nth-child(1) > button:nth-child(1)'):
        if 'CHF' in e.span.get_text():  #same as e.find('span).get_text()
            price = e.get_text()
            print(f'price: "{price}" in {e}')

    detail.find('span')






if __name__ == '__main__':
    run()