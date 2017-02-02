import scrapy
from loginform import fill_login_form
from scrapy import Selector,Spider
from fastweb.items import FastwebItem
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor
class MySpider(CrawlSpider):
    name = "fastweb"
    allowed_domains = ["fastweb.com"]
    start_urls = [
        #"https://www.fastweb.com"
        #"http://www.fastweb.com/college-scholarships/featured-scholarships"
        #"http://www.fastweb.com/college-scholarships/scholarships/169051",
    ]
    rules = (Rule(LinkExtractor(allow=(),restrict_xpaths=('//div[@class="next_scholarship"]/a/@href')), callback="parse_scholar", follow=True),)

    urls = []
    login_url = 'http://www.fastweb.com/login'
    login_user = 'xxx'
    login_password = 'xxx'

    def start_requests(self):
        yield scrapy.Request(self.login_url, self.parse_login)

    def parse_login(self, response):
        data, url, method = fill_login_form(response.url,response.body, self.login_user, self.login_password)

        return scrapy.FormRequest(url, formdata = dict(data), method = method , callback = self.bypassad)

    def bypassad(self,response):
        if response.url != "http://www.fastweb.com":
            yield scrapy.Request(url="http://www.fastweb.com/",callback=self.start_crawl)
        else:
            yield scrapy.Request(url="http://www.fastweb.com/",callback=self.start_crawl)
    def start_crawl(self, response):
        print("response after login ----->", response)

        sel = Selector(response)
        urls = sel.xpath("//p[@class='scholarship_name']/a/@href").extract()
        print "urls after login -----> " , urls
        for u in urls:
            self.start_urls.append(response.urljoin(u))
        for url in self. start_urls:
            yield scrapy.Request(url=url, callback=self.parse_scholar)

    def parse_scholar(self, response):
        print "url to crawled -----> " + response.url
        item = FastwebItem()
        sel = Selector(response)
        # page = response.url.split("/")[-2]
        # filename = 'fastweb-%s.html' % page
        #
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        award, deadline = sel.xpath("//p[@class='info']/text()").extract()
        next_page = sel.xpath("//div[@class='next_scholarship']/a/@href").extract_first()

        item['title'] = sel.xpath("//div[@class=\"title\"]/h1/text()").extract_first()
        item['description'] = sel.xpath("//div[@class='description']/text()").extract_first()
        item['award'] = award
        item['deadline'] = deadline
        item['link'] = sel.xpath("//div[@class='apply']/a/@href").extract_first()
        yield item
        if next_page is not None :
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_scholar)


