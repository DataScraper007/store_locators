import gzip
import json
import os
from lxml import html

import pandas as pd
from datetime import datetime
import scrapy
from scrapy.cmdline import execute

from store_locators.items import StoreLocatorsItem


class HusqvarnaSpider(scrapy.Spider):
    name = "husqvarna"

    def __init__(self):
        super().__init__()
        self.datetime = datetime.now().strftime('%Y%m%d')
        self.page_save = fr"C:\Users\Admin\PycharmProjects\page_save\store_locators\{self.datetime}\{HusqvarnaSpider.name}"

    def start_requests(self):
        df = pd.read_excel(r"C:\Users\Admin\PycharmProjects\store_locators\store_locators\states_store_locator.xlsx")
        for index, row in df.iterrows():
            yield scrapy.Request(
                url=f"https://maps.locations.husqvarna.com/api/getAsyncLocations?template=professional&level=search&search={row['address']}",
                cb_kwargs={"state":row['abbreviation']}
            )

    def parse(self, response, **kwargs):
        json_data = json.loads(response.text)
        file_path = self.page_save + '\\' + kwargs['state'] + ".html.gz"

        if not os.path.exists(self.page_save):
            os.makedirs(self.page_save)
        with gzip.open(file_path, 'wb') as file:
            file.write(response.body)


        item = StoreLocatorsItem()
        if json_data['maplist']:
            raw_data = html.fromstring(json_data['maplist']).xpath('//div[@class="tlsmap_list"]/text()')[0]
            store_data = json.loads(f"[{raw_data.rstrip(',')}]")
            for data in store_data:
                print(data)
                item['state'] = data['region']
                if item['state'] == kwargs['state']:
                    item['store_id'] = data['fid']
                    item['name'] = data['location_name']
                    item['latitude'] = data['lat']
                    item['longitude'] = data['lng']
                    item['street'] = data['address_1']
                    item['city'] = data['city']
                    item['zip_code'] = data['post_code']
                    item['country'] = 'USA'
                    item['county'] = ''
                    item['phone'] = data['local_phone_pn_dashes']
                    item['open_hours'] = ''
                    item['url'] = data['url']
                    item['provider'] = 'Husqvarna'''
                    item['category'] = 'Automobile Dealers'
                    item['updated_date'] = datetime.today().strftime('%d-%m-%Y')
                    item['status'] = ''
                    item['direction_url'] = ''
                    yield item



if __name__ == '__main__':
    execute(f'scrapy crawl {HusqvarnaSpider.name}'.split())
