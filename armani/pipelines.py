# -*- coding: utf-8 -*-
import time


class ArmaniPipeline(object):

    def open_spider(self, spider):
        self.time_stump = time.time()
        return spider

    def process_item(self, item, spider):
        item['crawl_time'] = time.time() - self.time_stump
        self.time_stump = time.time()
        return item
