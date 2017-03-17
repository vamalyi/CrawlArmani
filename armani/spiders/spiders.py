import scrapy
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class ArmaniSpider(CrawlSpider):
    name = "armani"
    allowed_domains = ['armani.com']

    rules = (
        Rule(LinkExtractor(allow=('_cod', )), callback='parse_main'),
        Rule(LinkExtractor(allow=(
            '/women$', 
            '/men$', 
            '/armanijunior', 
            'kids/secondary$',
            '/onlinestore/',
            ), unique=True), follow=True),
    )

    def __init__(self, *a, **kw):
        super(ArmaniSpider, self).__init__(*a, **kw)
        self._get_regions()

    def _get_regions(self):
        selected_regions = getattr(self, 'region', None)
        if selected_regions:
            self.start_urls = ['http://www.armani.com/{}'.format(rgn) for rgn in selected_regions.split('/')]
        else:
            self.start_urls = ['http://www.armani.com/{}'.format(get_project_settings.get('DEFAULT_REGION'))]

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
            if query.css('button::text').extract_first():
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
            'region': response.url.split("/")[3],
            'description': get_list(response.css('ul.descriptionList')),
        }
