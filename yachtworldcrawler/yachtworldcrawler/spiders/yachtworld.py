# -*- coding: utf-8 -*-
import scrapy
from yachtworldcrawler.items import YachtworldcrawlerItem

SEARCH_URL = "/core/listing/cache/searchResults.jsp?cit=true&slim=quick&ybw=&sm=3&searchtype=advancedsearch&Ntk=boatsEN&Ntt=&is=false&man=&hmid=0&ftid=101&enid=0&type=%28Sail%29&fromLength=36&toLength=43&fromYear=1990&toYear=&fromPrice=60%2C000&toPrice=90%2C000&luom=126&currencyid=1004&city=&rid=119&rid=151&pbsint=&boatsAddedSelected=-1"

class YachtworldSpider(scrapy.Spider):
    name = "yachtworld"
    allowed_domains = ["yachtworld.com"]
    start_urls = (
        'http://www.yachtworld.com' + SEARCH_URL,
    )

    def parse(self, response):

        # paging

        for href in response.css("span.navPage > a::attr('href')"):
           url = response.urljoin(href.extract())
           yield scrapy.Request(url, callback=self.parse)

        for href in response.css("div.make-model > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_model)

    def parse_model(self, response):

        item = YachtworldcrawlerItem()


        cont_main = response.xpath("//div[@class='content_main']")

        item['price_full'] = cont_main.xpath("div/div[@class='boat-price']/text()").extract()[0]
        item['name'] = cont_main.xpath("div/div[@class='boat-title']/h1/text()").extract()[0]

        item['year'] = cont_main.xpath("//dt[text() = 'Year:']/following-sibling::dd/text()").extract()[0]
        item['loa'] = cont_main.xpath("//dt[text() = 'Length:']/following-sibling::dd/text()").extract()[0]
        item['price'] = cont_main.xpath("//dt[text() = 'Current Price:']/following-sibling::dd/text()").extract()[0]
        item['id'] = cont_main.xpath("//dt[text() = 'YW#:']/following-sibling::dd/text()").extract()[0]
        item['url'] = response.url
        item['located'] = cont_main.xpath("//dt[text() = 'Located In:']/following-sibling::dd/text()").extract()[0]
        item['hull_material'] = cont_main.xpath("//dt[text() = 'Hull Material:']/following-sibling::dd/text()").extract()[0]

        spec_texts_raw = response.xpath("//div[contains(@class,'fullspecs')]/div/text()").extract()
        spec_texts = [t.strip() for t in spec_texts_raw if len(t.strip())>0]
        specs = dict([ [x.strip() for x in s.split(":")] if ":" in s else [s,""]  for s in spec_texts])

        item['full_specs'] = specs

        yield item