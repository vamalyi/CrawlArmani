import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class QuotesSpider(CrawlSpider):
    name = "quotes"
    allowed_domains = ['armani.com']
    start_urls = ['http://www.armani.com/us']

    rules = (
        Rule(LinkExtractor(allow=(
            '/women$', 
            '/men$', 
            '/armanijunior', 
            'kids/secondary$',
            '/onlinestore/',
            ), unique=True), follow=True),
        # Rule(LinkExtractor(allow=('/women$', '/onlinestore/',)), follow=True),

        Rule(LinkExtractor(allow=('_cod', )), callback='parse_main'),
    )

    
    # def start_requests(self):
    # #     urls = [
    # #         # 'http://quotes.toscrape.com/page/1/',
    # #         # 'http://www.armani.com/us',
    # #         'http://www.armani.com/us/emporioarmani/crewneck-sweater_cod39692915ji.html'
    # #         # 'http://quotes.toscrape.com/page/2/',
    # #     ]
    #     headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse_main(self, response):
        def get_list(query):
            return ' - '.join([item for item in query.css('li a::text').extract()]).replace('\t', ' ').replace('\n', ' ')
        
        def get_list_with_inner(query):
            return ','.join([item for item in query.css('li::text').extract()]).replace('\t', ' ').replace('\n', ' ')

        yield {
            'name': response.css('h1.productName::text').extract_first(),
            'price': response.css('span.priceValue::text').extract_first(),
            'currency': response.css('div.newprice::text').extract_first(),
            'category': '',
            'sku': response.css('span.MFC::text').extract_first(),
            # 'active': extract_css('div.qtyAvailability::text'),
            'color': get_list_with_inner(response.css('ul.Colors')),
            'size': get_list_with_inner(response.css('ul.SizeW')),
            'region': response.css('a.shippingTo::text').extract_first(),
            'description': get_list(response.css('ul.descriptionList')),
            'crawl_time': ''
        }

        
            # for item in query:
                
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        # 'name':
        # 'price':
        # 'currency':
        # 'category':
        # 'sku':
        # 'active':
        # 'crawl_time':
        # 'color':
        # 'size':
        # 'region':
        # 'description':
