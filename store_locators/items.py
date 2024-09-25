import scrapy


class StoreLocatorsItem(scrapy.Item):
    store_id = scrapy.Field()
    name = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    county = scrapy.Field()
    phone = scrapy.Field()
    open_hours = scrapy.Field()
    url = scrapy.Field()
    provider = scrapy.Field()
    category = scrapy.Field()
    updated_date = scrapy.Field()
    country = scrapy.Field()
    status = scrapy.Field()
    direction_url = scrapy.Field()

