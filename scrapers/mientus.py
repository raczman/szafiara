from array import array
from scrapers.utils import formatPrice, calcDiscount, convertCurrency
from models import Item
import requests
from bs4 import BeautifulSoup

def mientus(url: str) -> list[Item] :
    ret = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('div', class_='product--box box--minimal')

    for i in items:
        ret.append(parseItem(i))

    return ret

def parseItem(soup: BeautifulSoup) -> Item:
    pHead = soup.find('div', class_='product--head')

    url = pHead.find('a', class_='product--image').get('href')
    image = pHead.find('img').get('srcset').split(',')[0]

    productName = soup.find('a', class_='product--title').text
    make = soup.find('a', class_='product--supplier').find('strong').text.upper()

    price = formatPrice(soup.find('span', class_='price--default is--nowrap is--discount').text) / 100
    price_alt = formatPrice(soup.find('span', class_='price--discount is--nowrap').text) / 100
    price = convertCurrency(price, 'EUR')
    price_alt = convertCurrency(price_alt, 'EUR')
    discount = calcDiscount(price, price_alt)
    sizes = []

    for li in pHead.find_all('li'):
        if li.get('class') == 'disabled':
            continue
        sizes.append(li.text.upper())

    return Item(make, productName, price, price_alt, discount, url, image, 'mientus', sizes)