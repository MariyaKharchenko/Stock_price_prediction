import requests
from lxml import html
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
url = 'https://cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.From=01.01.2020&UniDbQuery.To=02.11.2024'

try:
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    table_data = dom.xpath("//table[@class='data']//tr")

    field_names = ['date', 'rate']
    with open("key_rate.csv", "a", encoding='utf8') as w_file:
        writer = csv.DictWriter(w_file, fieldnames=field_names)
        writer.writeheader()

        for row in table_data:
            cells = row.xpath(".//td/text()")
            if len(cells) == 2:
                date = cells[0].strip()
                rate = cells[1].strip()
                writer.writerow({'date': date, 'rate': rate})

except requests.exceptions.HTTPError as e:
    print("Response not 200:", e)