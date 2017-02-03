import scrapy
from loginform import fill_login_form
from scrapy import Selector,Spider

from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor
class MySpider(CrawlSpider):
    name = "fastweb"
    allowed_domains = ["fastweb.com"]
    start_urls = [
        "http://www.fastweb.com/directory/scholarships-for-korean-students"
    ]
    rules = (
        Rule(LinkExtractor(allow=('college-scholarships/scholarships/',)), callback='parse_item', follow=True),
    )
    target = open("urls.csv",'w')

    def parse_item(self,response):
        self.target.write(response.url + "\n")

