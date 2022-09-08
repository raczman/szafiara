from weakref import ref
from flask import Flask, render_template, jsonify
from models import Item
from scrapers import *


CONFIG = {
    'breuninger': [
        'https://www.breuninger.com/pl/marki/cp-company/+meskie/?sale=sale',
        'https://www.breuninger.com/pl/marki/stone-island/?sale=sale',
        'https://www.breuninger.com/pl/marki/stone-island-shadow-project/+meskie/?sale=sale',
        'https://www.breuninger.com/pl/marki/barbour/+meskie/?sale=sale',
        'https://www.breuninger.com/pl/marki/fred-perry/+meskie/?sale=sale',
        'https://www.breuninger.com/pl/marki/a-cold-wall/+meskie/?sale=sale'
    ],
    'showroom': [
        'https://www.showroom.pl/meska/stone-island/sale',
        'https://www.showroom.pl/brands/weekend-offender?sale=1',
        'https://www.showroom.pl/brands/lyle-scott?sale=1',
        'https://www.showroom.pl/brands/cp-company?sale=1',
        'https://www.showroom.pl/brands/barbour?sale=1'
    ],
    'vitkac':[
        'https://www.vitkac.com/pl/sklep/mezczyzni?targets=topFilter%2CproductList%2Coffsets_bottom&params%5B0%5D%5Bname%5D=proj%5B45%5D&params%5B0%5D%5Bvalue%5D=on&params%5B1%5D%5Bname%5D=proj%5B700%5D&params%5B1%5D%5Bvalue%5D=on&params%5B2%5D%5Bname%5D=discount%5B1%5D&params%5B2%5D%5Bvalue%5D=on&main_category=&undefined='
    ],
    'mientus':[
        'https://www.mientus.com/en/stone-island/?p=1&o=3&n=12&cf=2286%7C2287%7C2288%7C2293%7C2299%7C2304%7C2310%7C2315%7C2322'
    ],
    'martist': [
        'https://marshallartist.co.uk/category/sale/'
    ]
}

szmaty = []
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def refresh():
    global szmaty
    szmaty = []

    for shop in CONFIG.keys():
        print(f'Refreshing {shop} listings...')
        for link in CONFIG[shop]:
            if shop not in SCRAPERS:
                print(f'Cannot find scraper for {shop}!')
                continue
            print(f'Fetching {link}')
            szmaty.extend(SCRAPERS[shop](link))
        print(f'Listings for {shop} refreshed!')

    szmaty = [s._asdict() for s in szmaty]

SCRAPERS = {
    'breuninger': breuninger,
    'showroom': showroom,
    'vitkac': vitkac,
    'mientus': mientus,
    'martist': martist
}

@app.route('/')
def index():
    global szmaty
    return render_template('index.html', listings = szmaty)

@app.route('/data')
def data():
    global szmaty
    return jsonify(szmaty)

if __name__ == '__main__':
    refresh()
    app.run()
