from datetime import datetime
import json
import scrapy
from scrapy import Request
from scrapy.cmdline import execute

from store_locators.items import StoreLocatorsItem


class CricketWirelessSpider(scrapy.Spider):
    name = "cricket_wireless"

    def __init__(self):
        super().__init__()
        self.cookies = None
        self.headers = None
        self.datetime = datetime.now().strftime('%Y%m%d')
        self.page_save = fr"C:\Users\Admin\PycharmProjects\page_save\store_locators\{self.datetime}\{CricketWirelessSpider.name}"

    def start_requests(self):

        # self.cookies =
        # self.headers =

        yield scrapy.Request(
            url="https://api.momentfeed.com/v1/analytics/api/llp/cricket.json?auth_token=IVNLPNUOBXFPALWE&center=47.072515,-109.172599&coordinates=44.11377676094452,-98.75755993750049,49.87566219191183,-119.58763806250039&multi_account=false&name=Cricket+Wireless+Authorized+Retailer,Cricket+Wireless+Store&page=1&pageSize=50&type=store",
            # headers=self.headers,
            # cookies=self.cookies,
            callback=self.parse,
            cb_kwargs={"current_page": 1}
        )

    def parse(self, response, **kwargs):
        product_data = json.loads(response.text)
        location = kwargs['location']
        item = StoreLocatorsItem()
        if product_data:
            for data in product_data:
                item['state'] = data['store_info']['region']
                if item['state'] == location['state']:
                    item['store_id'] = data['store_info']['external_store_code']
                    item['name'] = data['store_info']['name']
                    item['latitude'] = data['store_info']['lat']
                    item['longitude'] = data['store_info']['lon']
                    item['street'] = " ".join(data['store_info']['address_text_lines'][:-1])
                    item['city'] = data['store_info']['locale']['name']
                    item['zip_code'] = data['store_info']['address_postcode']
                    item['country'] = 'USA'
                    item['county'] = ''
                    item['phone'] = data['store_info']['phone']
                    item['open_hours'] = " | ".join(data['store_info']['all_opening_hours']['schemaHrs'])
                    item['url'] = data['store_info']['website']
                    item['provider'] = "T-Mobile"
                    item['category'] = "Computer And Electronics Stores"
                    item['updated_date'] = datetime.today().strftime('%d-%m-%Y')
                    item['status'] = data['store_info']['status']
                    item['direction_url'] = data['store_info']['get_directions_link']
                    yield item

            total_pages = json_data['business_list']['paginator']['num_pages']
            next_page = kwargs['current_page'] + 1 if total_pages >= (kwargs['current_page'] + 1) else None
            if next_page:
                yield scrapy.Request(
                    url=f"",
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    cb_kwargs={"current_page": next_page}
                )


if __name__ == '__main__':
    execute(f'scrapy crawl {CricketWirelessSpider.name}'.split())
