from scrapers.utils import calcDiscount, formatPrice, http_get
from bs4 import BeautifulSoup
from models import Item
import json

def vitkac(url: str) -> list[Item]:
    res = http_get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.findAll('div', class_='product-media-query')

    ret = []
    for i in items:
        try:
            ret.append(vitkacItemParser(i, url))
        except Exception as e:
            print('Error while parsing item!')
            print(e)
            print(i)
            print('-----------------')

    return ret

def vitkacItemParser(item: BeautifulSoup, url: str) -> Item:
    id = item.find('a').get('data-seoid')
    make = item.find('h4').text.upper()
    name = item.find('span', class_='opis').find('p').text
    price = formatPrice(item.find('label', class_="sale").find(text=True))
    price_alt = formatPrice(item.find('label', class_='sale').find('span').text)
    url = item.find('a').get('href')
    image = item.find('img', class_='lazy first').get('data-src')

    prodDetail = http_get('https://www.vitkac.com/product_show/axNewQuickView?id=' + id,
    {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': url
    }).json()
    
    prodDetail = prodDetail['sizes']
    prodDetail = BeautifulSoup(prodDetail, 'html.parser')
    sizes = []

    for li in prodDetail.find_all('li'):
        size = li.get('data-value')
        if 'disabled' in li.get('class'):
            continue
        sizes.append(size.upper())

    return Item(make, name, price, price_alt, calcDiscount(price, price_alt), url, image, 'vitkac', sizes)
