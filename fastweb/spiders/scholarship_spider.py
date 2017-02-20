import scrapy
from loginform import fill_login_form
from scrapy import Selector,Spider

from scrapy.spiders import CrawlSpider, Rule
from fastweb.items import FastwebItem
from scrapy.linkextractors import LinkExtractor
class MySpider(CrawlSpider):
    name = "scholarships"
    allowed_domains = ["scholarships.com"]
    start_urls = [
        "https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/"
    ]
    rules = (
        Rule(LinkExtractor(allow=('/college-scholarships/scholarship-directory/',)), callback='parse_item', follow=True),
    )
    # target = open("urls.csv",'w')

    def parse_item(self,response):
        sel = Selector(response)
        data = sel.xpath("//div[@id='divscholdetails']/ul/li/text()").extract()
        address = sel.xpath("//a[@class='award']/text()").extract()
        title = sel.xpath("//div[@id='divlist']/h1/text()").extract()

        if len(address) != 0 :
            item = FastwebItem()
            iDescription = data.index("Scholarship Description")
            if (len(data) > iDescription):
                description = data[iDescription + 1]
            else:
                description = ''
            iAward = data.index("Maximum Amount")
            if (data[iAward + 1] != "Scholarship Description"):
                award = data[iAward + 1]
            else:
                award = ''
            iDeadline = data.index("Application Deadline")
            if (data[iDeadline + 1] != "Number Of Awards"):
                deadline = data[iDeadline + 1]
            else:
                deadline = ''

            item['title'] = title[0]
            item['description'] = description
            item['award'] = award[:]
            item['deadline'] = deadline
            item['link'] = address[0]
            yield item
        else:
            pass
        # self.target.write(response.url + "\n")
