import json

import pymysql
import scrapy
from scrapy.cmdline import execute
import pandas as pd


class LatLongSpider(scrapy.Spider):
    name = "lat_long"

    def __init__(self):
        super().__init__()

        db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': 'actowiz',
            'db': 'store_locators'
        }

        self.connection = pymysql.connect(**db_params)
        self.cursor = self.connection.cursor()


    def start_requests(self):
        api_key = "AIzaSyCfgmJmWqeHZFJGOevrMoARaNt3sBFPxxE"

        locations = pd.read_excel(r"C:\Users\Admin\PycharmProjects\store_locators\states.xlsx")

        for index, location in locations.iterrows():
            yield scrapy.Request(
                url=f"https://maps.googleapis.com/maps/api/geocode/json?address={location['state']}&key={api_key}",
                callback=self.parse,
                cb_kwargs={"location": location}
            )

    def parse(self, response, **kwargs):
        api_response_dict = json.loads(response.text)
        print(api_response_dict)
        state = kwargs['location']['state']
        lat = kwargs['location']['lat']
        long = kwargs['location']['long']
        short_name = api_response_dict['results'][0]['address_components'][0]['short_name']
        self.cursor.execute("INSERT IGNORE INTO lat_long (state, lat, `long`, short_name) values (%s,%s,%s,%s)", (state, lat, long, short_name))
        self.connection.commit()

if __name__ == '__main__':
    execute(f'scrapy crawl {LatLongSpider.name} -s CONCURRENT_REQUESTS=1'.split())
