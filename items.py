# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EngineItem(scrapy.Item):
    # define the fields for your item here like:
    # Metadata
    crawler_id = scrapy.Field()
    car_id = scrapy.Field()

    # Car details
    site = scrapy.Field()
    marca = scrapy.Field()
    modelo = scrapy.Field()
    agno = scrapy.Field()
    moneda = scrapy.Field()
    precio = scrapy.Field()
    motor = scrapy.Field()
    kilometraje = scrapy.Field()
    color = scrapy.Field()
    transmision = scrapy.Field()
    link = scrapy.Field()

    # Images
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_name = scrapy.Field()
