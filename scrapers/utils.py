import re
from tokenize import Double
from currency_converter import SINGLE_DAY_ECB_URL, CurrencyConverter
from requests_toolbelt.utils import dump
import requests

__cconverter = CurrencyConverter(SINGLE_DAY_ECB_URL)

def convertCurrency(amount: Double, currency: str) -> Double:
    return __cconverter.convert(amount, currency, 'PLN')

def formatPrice(price: str) -> int:
    if price is None:
        return None
    price = price.replace('.', '')
    price = price.replace(',', '.')
    return int(float(re.sub("[^0-9.]", "", price)))


def calcDiscount(price, price_alt):
    return "-" + str(int(100 - ((price/price_alt) * 100))) + "%"

def pretty_print_request(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

httpSession = requests.Session()

def http_get(url, headers={}, debug=False):
    headers_for_req = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50'
    }

    resp =  httpSession.get(url, headers={**headers_for_req, **headers})
    if debug == True:
        data = dump.dump_all(resp)
        print(data.decode('utf-8'))
    return resp