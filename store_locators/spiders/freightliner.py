import gzip
import json
import os
from urllib.parse import urlencode

import pytz
from lxml import html
import pandas as pd
from datetime import datetime
import scrapy
from scrapy.cmdline import execute
import pymysql

from store_locators.items import StoreLocatorsItem


class FreightlinerSpider(scrapy.Spider):
    name = "freightliner"

    def __init__(self):
        super().__init__()
        db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': 'actowiz',
            'db': 'store_locators'
        }
        self.conn = pymysql.connect(**db_params)
        self.cur = self.conn.cursor()
        self.datetime = datetime.now().strftime('%Y%m%d')
        self.page_save = fr"C:\Users\Admin\PycharmProjects\page_save\store_locators\{self.datetime}\{FreightlinerSpider.name}"

    def start_requests(self):
        self.cur.execute("SELECT north, south, east, west, state, abbreviation FROM coordinates")
        results = self.cur.fetchall()

        for data in results:
            north, south, east, west, state, abbreviation = data
            params = {
                "north": north,
                "south": south,
                "east": east,
                "west": west
            }
            yield scrapy.Request(
                url='https://www.freightliner.com/umbraco/backoffice/dealers/geo-search?' + urlencode(params),
                cb_kwargs={"state": abbreviation},
                callback=self.parse
            )

    # Helper function to convert time in minutes to 24-hour format
    def convert_to_24_hour_format(self, minutes):
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02}:{mins:02}"

    # Function to format the data as required
    def format_hours(self, data):
        output = []
        for day, info in data.items():
            if info["status"] == "Open":
                open_time = self.convert_to_24_hour_format(info["open"])
                close_time = self.convert_to_24_hour_format(info["close"])
                output.append(f"{day}: {open_time}-{close_time}")
            else:
                output.append(f"{day}: closed")
        return " | ".join(output)

    def format_direction_url(self, data):
        return "https://www.google.com/maps/?" + f"q={data['address']}, {data['city']}, {data['state']} {data['zip']}, {data['state']}, {data['country']} {data['zip']} <br> {data['city']}, {data['state']}, {data['country']} {data['zip']}"

    def parse(self, response, **kwargs):
        file_path = self.page_save + '\\' + kwargs['state'] + ".html.gz"

        if not os.path.exists(self.page_save):
            os.makedirs(self.page_save)
        with gzip.open(file_path, 'wb') as file:
            file.write(response.body)

        product_data = json.loads(response.text)
        item = StoreLocatorsItem()
        if product_data:
            for data in product_data:
                item['state'] = data['state']
                if item['state'] == kwargs['state']:
                    item['store_id'] = data['code']
                    item['name'] = data['name']
                    item['latitude'] = data['latitude']
                    item['longitude'] = data['longitude']
                    item['street'] = data['address']
                    item['city'] = data['city']
                    item['zip_code'] = data['zip']
                    item['country'] = 'USA'
                    item['county'] = ''
                    item['phone'] = data['phone']

                    # Convert data to the desired format
                    # item['open_hours'] = ''
                    for type in data['departments']:
                        if type['name'] == 'Sales':
                            item['open_hours'] = self.format_hours(type['schedule'])
                            break
                    else:
                        return
                            # if type['type'] == 'Parts':
                            #     item['open_hours'] = self.format_hours(type['schedule'])
                            # else:
                            #     item['open_hours'] = self.format_hours(type['schedule'])

                    item['url'] = f"https://www.freightliner.com/Dealer?code={data['code']}&name={data['name']}"
                    item['provider'] = "Freightliner"
                    item['category'] = "Automobile Dealers"
                    item['updated_date'] = datetime.today().strftime('%d-%m-%Y')
                    if item.get('open_hours'):
                        item['status'] = 'Open' if self.parse_hours(item['open_hours']) else 'Closed'
                    else:
                        item['status'] = 'Closed'
                    item['direction_url'] = self.format_direction_url(data)
                    yield item

    def parse_hours(self, hours_string):
        # Split the string into days and times
        days_hours = hours_string.split(" | ")
        store_hours = {}

        # Process each day's hours
        for day_hour in days_hours:
            day, hours = day_hour.split(": ")
            store_hours[day] = hours

        return self.is_store_open(store_hours)

    def is_store_open(self, store_hours):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        current_day = now.strftime("%A").lower()
        current_time = now.strftime("%H:%M")

        if store_hours.get(current_day) == "closed":
            return False

        opening_time, closing_time = store_hours[current_day].split("-")

        return opening_time <= current_time <= closing_time


if __name__ == '__main__':
    execute(f'scrapy crawl {FreightlinerSpider.name}'.split())
