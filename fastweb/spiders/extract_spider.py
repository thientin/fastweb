import scrapy
from loginform import fill_login_form
from scrapy import Selector,Spider
from fastweb.items import FastwebItem
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor
class MySpider(CrawlSpider):
    name = "extractspider"
    allowed_domains = ["fastweb.com"]
    start_urls = [
    ]
    rules = (Rule(LinkExtractor(allow=(),restrict_xpaths=('//div[@class="next_scholarship"]/a/@href')), callback="parse_scholar", follow=True),)
    file = open("urls.csv","r")
    for i in file:
        start_urls.append(i)
    urls = []
    login_url = 'http://www.fastweb.com/login'
    login_user = 'dungle@goappable.com'
    login_password = 'testing123'

    def start_requests(self):
        yield scrapy.Request(self.login_url, self.parse_login)

    def parse_login(self, response):
        data, url, method = fill_login_form(response.url,response.body, self.login_user, self.login_password)

        return scrapy.FormRequest(url, formdata = dict(data), method = method , callback = self.start_crawl)

    def start_crawl(self, response):
        for url in self. start_urls:
            yield scrapy.Request(url=url, callback=self.parse_scholar)

    def parse_scholar(self, response):
        print "url to crawled -----> " + response.url
        item = FastwebItem()
        sel = Selector(response)
        award, deadline = sel.xpath("//p[@class='info']/text()").extract()
        next_page = sel.xpath("//div[@class='next_scholarship']/a/@href").extract_first()

        item['title'] = sel.xpath("//div[@class=\"title\"]/h1/text()").extract_first()
        item['description'] = sel.xpath("//div[@class='description']/text()").extract_first()
        item['award'] = award
        item['deadline'] = deadline
        item['link'] = sel.xpath("//div[@class='apply']/a/@href").extract_first()
        yield item