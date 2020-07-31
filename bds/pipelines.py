# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymssql
import re
from scrapy.exceptions import DropItem

class BdsPipeline(object):

    def __init__(self):
        self.conn = pymssql.connect(host='localhost:1433', user='sa', password='123456', database='BDS')
        self.cursor = self.conn.cursor()
        

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            for data in item:
                if not data:
                    is_valid = False
                    raise DropItem("Missing %s!" % data)
        
        if is_valid:
            valid_data = True
            try:
                title = re.sub('\r|\n','',item['title']).lower()
                square = re.sub('\r|\n|m²','',item['square'])
                category = re.sub('\r|\n','',item['category'])
                dateCreate = re.sub('\r|\n','',item['dateCreate'])
                price = re.sub('\r|\n|\xa0','',item['price'])
                price_num = float(re.findall('\d+\.?\d+|\d+',price)[0])
                if 'tỷ' in price:
                    price_num *= 1000
                if '/m²' not in price:
                    price = str(price_num / float(square))
                else:
                    price = str(price_num)
            
            except:
                raise DropItem("Error Format Data!")
                valid_data = False
                pass
            try:
                if (valid_data):
                    select = 'SELECT title FROM Estate Where title like %s and dateCreate like %s'
                    self.cursor.execute(select,((title),(dateCreate)))
                    existence = self.cursor.fetchall()
                    if existence:
                        raise DropItem("Data exited!")
                    else:
                        sql = 'INSERT INTO Estate(title,square,price,category,longitude,latitude,dateCreate,address) VALUES(%s, %s, %s, %s,%s,%s,%s,%s)'
                        # //self.cursor.execute(sql,((item['title']),(item['square']),(item['price']),(item['category']),(item['longitude']),(item['latitude']),(item['dateCreate']),(item['address'])))
                        self.cursor.execute(sql,((title),(square),(price),(category),(item['longitude']),(item['latitude']),(dateCreate),(item['address'])))
                        self.conn.commit()
                valid_data = True
            except:
                raise DropItem("SQL Error!")
        return item
