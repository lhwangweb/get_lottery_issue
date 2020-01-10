# -*- encoding: utf-8 -*-
import scrapy
import scrapy_splash
from get_lottery_issue.items import GetLotteryIssueItem

class TxffcJsSpider(scrapy.Spider):
    """
    騰訊分分彩爬蟲 - JS 版 (使用 Splash)
    """
    name = "txffc_js"

    def start_requests(self):
        """
        爬蟲的執行主體
        """
        urls = [
            'http://www.tx-ffc.com/txffc/',
        ]

        _myheader = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }

        for url in urls:
            # 用 scrapy_splash 發起 Request -> 取得 response -> 透過 splash server 去執行頁面上的 js -> callback parse  -> parse 收到最終 response 並做頁面解析
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse, args={'wait': 0.5}, headers=_myheader)

    def parse(self, response):
        """
        解析器 - 解析 response 用 
           1. 因為用 Spalsh 處理過，因此這裡 response 內容為 Js Render 完成的結果
           2. 用 Selector 去 response 內把東西找出來
              - 我用 CSS 選擇器，語法接近 jQuery，另外也有 xpath 選擇器可以用。
              - 參考文件: http://doc.scrapy.org/en/latest/topics/selectors.html 
        """
        print("抓取 Rendor 過 JS 的 DOM 完成，開始解析頁面")
        print("時間 | 期號 | 開獎號")
        
        # 用選擇器選取目標，根據觀察: 這個 tr 每一 row 就是一期的資訊 
        issues = response.css("div.kj-info > div.kj-list > table > tbody > tr") 

        # 處理每一期
        for issue in issues:
            fields = issue.css("td")
            row_data = GetLotteryIssueItem()
            i = 1
            for field in fields:
                if i == 1:
                    row_data["datetime"] = " ".join(field.css("td > font::text").extract())
                elif i == 2:
                    row_data["serial_no"] = field.css("td::text").extract_first()
                elif i == 3:
                    row_data["issue_no"] = "".join(field.css("td > span::text").extract())
                elif i == 4:
                    row_data["bigger_smaller_no"] = "".join(field.css("td > span::text").extract())
                elif i == 5:
                    row_data["odd_even_no"] = "".join(field.css("td > span::text").extract())
                elif i == 6:
                    row_data["sum_1"] = field.css("td > font::text").extract_first()
                elif i == 7:
                    row_data["sum_2"] = field.css("td > font::text").extract_first()
                elif i == 8:
                    row_data["sum_3"] = field.css("td > font::text").extract_first()
                elif i == 9:
                    row_data["dragon"] = field.css("td > font::text").extract_first()
                elif i == 10:
                    row_data["f3"] = field.css("td > font::text").extract_first()
                elif i == 11:
                    row_data["m3"] = field.css("td > font::text").extract_first()
                elif i == 12:
                    row_data["b3"] = field.css("td > font::text").extract_first()
                i+=1
            
            if "datetime" in row_data and "serial_no" in row_data and "issue_no" in row_data and "bigger_smaller_no" in row_data and "odd_even_no" in row_data and "sum_1" in row_data and "sum_2" in row_data and "sum_3" in row_data and "dragon" in row_data and "f3" in row_data and "m3" in row_data and "b3" in row_data:
                print(row_data["datetime"] + " | " + row_data["serial_no"] + " | " + row_data["issue_no"])
                yield row_data
            else:
                if "datetime" in row_data:
                    print ("lose data ignore "+ row_data["datetime"]) 
                else:
                    print("empty row, ignore")
