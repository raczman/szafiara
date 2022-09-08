from scrapers.utils import calcDiscount, formatPrice
import requests
from bs4 import BeautifulSoup
from models import Item

def showroom(url: str) -> list[Item]:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('li', class_='p-listing-products__item')

    ret = []
    for i in items:
        try:
            ret.append(showroomItem(i))
        except Exception as e:
            print('Error while parsing item!')
            print(e)
            print(i)
            print('-----------------')
            continue

    return ret

SIZE_REPLACEMENT = {
    '2XL': 'XXL',
    '3XL': 'XXXL',
}

def showroomItem(s: BeautifulSoup) -> Item:
    make = s.find('span', class_='c-product-card__brand-link').text.strip().upper()
    product = s.find('span', class_='c-product-card__title-link').text.strip()

    price_alt = s.find('span', class_='c-product-card__price c-product-card__price--before')
    price = s.find('span', class_='c-product-card__price c-product-card__price--current')
    if price:
        price = formatPrice(price.text)
    else:
        price = formatPrice(s.find('span', class_='c-product-card__price').text)

    if price_alt:
        price_alt = formatPrice(price_alt.text)
    else:
        price_alt = price
    url = 'https://showroom.pl' + s.find('a', class_='c-product-card__text-link js-product-card-link').get('href')
    image = s.find('img', class_='c-product-card__image u-lazy / js-product-card-image').get('src').split('?')[0]
 
    sizes = []

    for span in s.find_all('span', class_='c-product-card__hover-size / js-variant-size'):
        size = span.text
        size = size.replace('W', '')

        sizes.append(size)

    return Item(make, product, price, price_alt,  calcDiscount(price, price_alt), url, image, 'showroom', sizes)

