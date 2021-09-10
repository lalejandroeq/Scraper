# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy import create_engine, MetaData, exc


class EnginePipeline:
    def __init__(self):
        self.start_timestamp = datetime.datetime.now()
        self.db_engine = create_engine('sqlite:///engine/cars.db')

    def process_item(self, item, spider):
        meta = MetaData()
        meta.reflect(bind=self.db_engine)
        table_keys = ['crawler_id', 'car_id', 'site', 'marca', 'modelo', 'agno', 'moneda', 'precio',
                      'motor', 'kilometraje', 'color', 'transmision', 'link']
        values = {key: item[key] for key in table_keys}
        values['insert_timestamp'] = self.start_timestamp
        conn = self.db_engine.connect()
        try:
            conn.execute(meta.tables['cars_tb'].insert().values(values))
        except exc.IntegrityError:
            spider.log('Car link already exists in DB')
        finally:
            conn.close()
        return item


class CarsImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'crawler_id': item["crawler_id"], 'image_name': item["image_name"]})
                for x in item.get('image_urls', [])]

    def file_path(self, request, response=None, info=None):
        return '{}/full/{}.jpg'.format(request.meta["crawler_id"], request.meta["image_name"])

    def thumb_path(self, request, thumb_id, response=None, info=None):
        return '{}/thumbs/{}/{}.jpg'.format(request.meta["crawler_id"], thumb_id, request.meta["image_name"])
