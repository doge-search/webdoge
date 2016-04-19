import scrapy


class proItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    office = scrapy.Field()
    phone = scrapy.Field()
    picture = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
