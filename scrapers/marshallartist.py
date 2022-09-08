from models import Item
from scrapers.utils import calcDiscount, formatPrice, http_get, convertCurrency
from bs4 import BeautifulSoup

def martist(url: str) -> list[Item]:
    ret = []
    page = 1
    res = http_get(url + f'/page/{page}')
    while res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.find('ul', class_='products columns-3').find_all('li')
        for i in items:
            try:
                print(i.get('class'))
                if i.get('class') is not None or 'type-product' in i.get('class'):
                    ret.append(parse_martist(i))
            except Exception as e:
                print('Error while parsing item!')
                print(e)
                print(i)
                print('-----------------')

        page += 1
        res = http_get(url + f'/page/{page}')
    return ret

def parse_martist(s: BeautifulSoup) -> Item:
    name = s.find('h2', class_='woocommerce-loop-product__title').text

    price_alt = formatPrice(s.find('del').find('span').text) / 100
    price = formatPrice(s.find('ins').find('span').text) / 100
    price = convertCurrency(price, 'GBP')
    price_alt = convertCurrency(price_alt, 'GBP')
    
    discount = calcDiscount(price, price_alt)
    url = s.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').get('href')
    image = s.find('img').get('src')
    sizes = []

    for s in s.find('div', class_='product-variations-size').find_all('span'):
        size = s.text.upper()
        sizes.append(size)

    ret = Item('MARSHALL ARTIST', name, price, price_alt, discount, url, image, 'marshallartist.co.uk', sizes)
    print(ret)

    return ret