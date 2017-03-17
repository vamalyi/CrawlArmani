# -*- coding: utf-8 -*-
import time
import pandas
import json


class ArmaniPipeline(object):

    def open_spider(self, spider):
        self.time_stump = time.time()
        return spider
    
    def process_item(self, item, spider):
        item['crawl_time'] = time.time() - self.time_stump
        self.time_stump = time.time()
        return item

    def close_spider(self, spider):
        data = pandas.read_csv('armani_crawl_data.csv')

        result = dict()

        us_products = data['region'] == 'us'
        fr_products = data['region'] == 'fr'

        us_usd = data['currency'] == 'USD'
        us_eur = data['currency'] == 'EUR'
        us_usd_count = len((data[us_products & us_usd]).index)
        us_eur_count = len((data[us_products & us_eur]).index)

        fr_usd = data['currency'] == 'USD'
        fr_eur = data['currency'] == 'EUR'
        fr_usd_count = len((data[fr_products & fr_usd]).index)
        fr_eur_count = len((data[fr_products & fr_eur]).index)

        result['product_count'] = {
            'USA': len(data[us_products].index), 'France': len(data[fr_products].index)
        }
        result['currency'] = {
            'USA': 'USD: {0} products, EUR: {1} products'.format(us_usd_count, us_eur_count),
            'France': 'EUR: {1} products, USD: {0} products'.format(fr_usd_count, fr_eur_count)
        }
        result['percentage'] = {
            'color': '{} %'.format(len((data['color'] != '').index) / len(data.index) * 100),
            'size': '{} %'.format(len((data['size'] != '').index) / len(data.index) * 100),
            'description': '{} %'.format(len((data['description'] != '').index) / len(data.index) * 100)
        }
        with open('test_result.json', 'w') as json_file:
            json.dump(result, json_file)
