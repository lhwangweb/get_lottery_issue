# -*- coding: utf-8 -*-
import MySQLdb

class GetLotteryIssuePipeline(object):
    """
    Pipline - 這邊只有一個任務就是寫入 MySQL
    """
    db_conn = None
    cursor = None
    
    def process_item(self, item, spider):
        """
        此 Pipeline 的執行本體，目前只進行一項工作: save_to_mysql
        """
        try:
            self.save_to_mysql(item)
        except Exception as e:
            print (e)
        return item

    def save_to_mysql(self, item):
        """
        存入 MySQL
        """
        if "datetime" in item:
            sql_h = "INSERT INTO `issue_data` (datetime, serial_no, issue_no, bigger_smaller_no, odd_even_no, sum_1, sum_2, sum_3, dragon, f3, m3, b3 ) VALUES ("
            sql_t = ");"
            sql_values = ",".join([
                "'" + item["datetime"] + "'",
                "'" + item["serial_no"] + "'",
                "'" + item["issue_no"] + "'",
                "'" + item["bigger_smaller_no"] + "'",
                "'" + item["odd_even_no"] + "'",
                "'" + item["sum_1"] + "'",
                "'" + item["sum_2"] + "'",
                "'" + item["sum_3"] + "'",
                "'" + item["dragon"] + "'",
                "'" + item["f3"] + "'",
                "'" + item["m3"] + "'",
                "'" + item["b3"] + "'",
            ])
            
            print(" - Saved")
            self.cursor.execute(sql_h + sql_values + sql_t)
            self.db_conn.commit()
    
    def open_spider(self, spider):
        """
        Pipeline Init 工作，例如 db connect
        """
        try:
            user = spider.settings.get('USERNAME')
            passwd = spider.settings.get('PASSWORD')
            self.db_conn = MySQLdb.connect(
                host="localhost",
                user=user, 
                passwd=passwd, 
                db="scrapy_data"
            )
            self.cursor = self.db_conn.cursor() 
            self.db_conn.set_character_set ( 'utf8mb4')
            self.cursor.execute ('SET NAMES utf8mb4;')
            self.cursor.execute ('SET CHARACTER SET utf8mb4;')
            self.cursor.execute ('SET character_set_connection=utf8mb4;')
        except:
            print("DB Connect Init Error")           
        
    def close_spider(self, spider):
        """
        Pipeline Close 工作，例如 db connect close
        """
        try:
            self.db_conn.close()
        except:
            print("DB Close Error")