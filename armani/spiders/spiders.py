import scrapy
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class QuotesSpider(CrawlSpider):
    name = "quotes"
    allowed_domains = ['armani.com']
    start_urls = ['http://www.armani.com/us']

    rules = (
        Rule(LinkExtractor(allow=('_cod', )), callback='parse_main'),
        Rule(LinkExtractor(allow=(
            # '/women$', 
            # '/men$', 
            '/armanijunior', 
            # 'kids/secondary$',
            # '/onlinestore/',
            ), unique=True), follow=True),
        # Rule(LinkExtractor(allow=('/women$', '/onlinestore/',)), follow=True),
    )

    # def start_requests(self):
    #     urls = [
    #         # 'http://quotes.toscrape.com/page/1/',
    #         # 'http://www.armani.com/us',
    #         'http://www.armani.com/us/emporioarmani/crewneck-sweater_cod39692915ji.html'
    #         # 'http://quotes.toscrape.com/page/2/',
    #     ]
  

    def parse_main(self, response):
        def get_list(query):
            return ' - '.join([item for item in query.css('li::text').extract()]).replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
        
        def get_list_with_inner(query):
            return ','.join([item for item in query.css('li a::text').extract()]).replace('\t', ' ').replace('\n', ' ')

        def get_currency(query):
            if query == '$':
                return 'USD'
            if query == 'EUR':
                return 'EUR'
            return 'None'

        def get_availability(query):
            if query.css('button::text').extract_first() == 'Add to Shopping Bag':
                return True
            return False


        yield {
            'name': response.css('h1.productName::text').extract_first(),
            'price': response.css('span.priceValue::text').extract_first(),
            'currency': get_currency(response.css('span.currency::text').extract_first()),
            'category': response.url.split("/")[4],
            'sku': response.css('span.MFC::text').extract_first(),
            'availability': get_availability(response.css('div.buttonBox')),
            'color': get_list_with_inner(response.css('ul.Colors')),
            'size': get_list_with_inner(response.css('ul.SizeW')),
            'region': response.css('a.shippingTo::text').extract_first(),
            'description': get_list(response.css('ul.descriptionList')),
        }

        # page = response.url.split("/")[1]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

