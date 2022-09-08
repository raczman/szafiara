from models import Item
import requests
from bs4 import BeautifulSoup
from scrapers.utils import calcDiscount, formatPrice


def breuninger(url: str) -> list[Item]:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.findAll('div', class_='suchen-produktliste__item')
    ret = []
    for i in items:
        try:
            ret.append(breuningerItemDetails(i))
        except Exception as e:
            print(e)
            continue

    return ret

def breuningerItemDetails(soup: BeautifulSoup) -> Item:
    make = soup.find('span', class_="suchen-produkt__marke").text.upper()
    product = soup.find('span', class_="suchen-produkt__name").text
    price_alt = soup.find('del', class_="suchen-preis suchen-preis--streichpreis produkt-preis__alt")
    if price_alt:
        price_alt = breuningerFormatPrice(price_alt.text)
        price = breuningerFormatPrice(soup.find('ins', class_="suchen-preis suchen-preis--rotpreis produkt-preis__aktuell").text)
    else:
        price = breuningerFormatPrice(soup.find('span', class_="produkt-preis__aktuell").text)
    
    url = 'https://www.breuninger.com' + soup.find('a').get('href')
    image = soup.find('img', class_='suchen-produkt__bild').get('data-src')
    if image is None:
        image = soup.find('img', class_='suchen-produkt__bild').get('src')
    image = image.split('?')[0]

    sizes = []
    data_sizes = soup.find('span', class_='suchen-produkt-farbkachel suchen-produkt-farbkachel--aktiv').get('data-sizes')
    data_sizes = data_sizes.replace(' ', '').replace('"', '').replace(']', '').replace('[','').upper()
    
    for s in data_sizes.split(','):
        if '=' in s:
            sizes.append(s.split('=')[0])
        else:
            sizes.append(s)

    return Item(make, product, price, price_alt, calcDiscount(price, price_alt), url, image, 'breuninger', sizes)

def breuningerFormatPrice(price: str) -> int:
    if price is None:
        return None
    return int(price.replace('\xa0', '').replace(' zł', ''))