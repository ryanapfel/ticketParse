# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class newEvent(scrapy.Item):
    eventDate = scrapy.Field()
    artistName = scrapy.Field()
    eventName = scrapy.Field()
    venueName = scrapy.Field()
    venueLocation = scrapy.Field()
    venueSize = scrapy.Field() # optional field of how large venue is
    saleStart = scrapy.Field() # needs to be a date object
    ticketArray = scrapy.Field() # contains all the information about ticket sales
