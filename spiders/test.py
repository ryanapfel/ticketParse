from __future__ import absolute_import
import scrapy
import logging
from scrapy import Selector
import datetime

class Test(scrapy.Spider):
    name = "Test"
    login_url = 'https://accounts.songkick.com/session/new'
    start_urls = [login_url]
    handle_httpstatus_list = [404]
    base_url = 'https//songkick.com'

    def parse(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username_or_email': 'guidomillikan@gmail.com', 'password': 'guidoB@sketbal123'},
            callback=self.after_login
        )

    def after_login(self,response):
        # get new show urls
        ##for k in response.xpath("//div[@id='recently-added']//div[@data-analytics_category='carousel_recently_added_v2']//span[@class='event-title']/text()").extract():
            ##yield {"event_name": k}
        urls = response.xpath("//div[@id='recently-added']//div[@data-analytics_category='carousel_recently_added_v2']//a/@href").extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_new_events)

    def parse_new_events(self,response):
        newItem = dict()
        newItem['eventDate'] = response.xpath("//*[@class='date-and-name']/p/text()").extract_first()
        newItem['artitstName'] = response.xpath("//h1/span/a/text()").extract_first()
        newItem['venueName'] = response.xpath("//*[@class='location']//span/a/text()").extract_first()
        newItem['venueLocation'] = response.xpath("(//*[@class='location']//span/text())[2]").extract_first()
        newItem['venueSize'] =  response.xpath("//span[@class='capacity']/text()").extract_first()
        newItem['saleStart'] = response.xpath("//span[@class='on-sale-time-copy']/text()").extract_first()

        # Get Ticket Information and store in ticket array
        ticketAr = []
        for ticket in response.xpath("//*[@id='tickets']//div").extract():
            rider = Selector(text=ticket)
            tempLink = rider.xpath("//a/@href").extract_first() # not the full link
            link = response.urljoin(tempLink) # extends the full url
            price = rider.xpath("//*[@class='price']/text()").extract_first() # price string is raw. price not always present. Must check later for its existence
            vendor = rider.xpath("//*[@class='vendor']/text()").extract_first()
            tempDic = {'Vendor': vendor,'Link': link,'Price': price}
            ticketAr.append(tempDic)

        newItem['ticketArray'] = ticketAr # adds the information from the pag

        yield newItem
