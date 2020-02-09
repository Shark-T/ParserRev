import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def write_csv(data):
    with open('revzilla.csv', 'a', newline='') as f:
        writer = csv.writer(f, dialect='excel', delimiter=';') # or lineterminator='\n'

        writer.writerow([data['name'],
                         data['style'],
                         data['item'],
                         data['code'],
                         data['price']])


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1', class_="product-show-details-name__name").text.strip()
    price = soup.find('div',
                      class_="product-show-details-pricing__price-retail product-details__price-retail mny__rng") \
                .find('span', class_='mny').text[1:].strip()
    trs = soup.find('table').find('tbody').find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')
        stl = tds[0].text.strip()
        style = stl.split(' ', maxsplit=2)[2].strip()
        it = tds[1].text.strip()
        item = it.split(' ', maxsplit=2)[2][1:].strip()
        cd = tds[2].text.strip()
        code = cd.split(' ', maxsplit=2)[2][1:].strip()
        data = {'name': name,
                'style': style,
                'item': item,
                'code': code,
                'price': price}

        write_csv(data)


def main():
    url = 'https://www.revzilla.com/motorcycle/shoei-rf-1200-helmet-solid'
    get_data(get_html(url))


if __name__ == '__main__':
    main()