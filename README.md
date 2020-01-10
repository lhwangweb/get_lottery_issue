## 主題

- 玩一下 Scrapy + Splash ，爬取需要執行 Js 才可以獲得真正結果的頁面。
- 以 [騰訊分分彩]('http://www.tx-ffc.com/txffc/) 首頁開獎資訊為範例。

## 技術說明

1. Python 2.7 + Scrapy + Splash (用 3.5 也可以，我用 2.7 純粹是懶得另外安裝 3 的環境)
2. 檔案與資料夾結構是預設的 Scrapy 專案架構，用指令 scrapy startproject get_lottery_issue 生成
   - 參考: https://docs.scrapy.org/en/latest/intro/tutorial.html


## 使用說明

### 一、 跑不處理 JS 的爬蟲
1. 安裝 Scrapy
   - 先生成一個 python 2.7 的 Virtual Environment，例如 env_27
   - 安裝 scrapy
      - 參考: https://docs.scrapy.org/en/latest/intro/install.html
   ```bash
   (env_27) user$ pip install scrapy
   ```
2. 執行爬蟲 (Location: get_lottery_issue/get_lottery_issue/spiders/txffc.py)
   - 可以發現這裡的結果來自原始 DOM，跟網頁最終看到的不同
   ```bash
   (env_27) user$ cd get_lottery_issue # 這是第一層 get_lottery_issue， README 這層
   (env_27) user$ scrapy crawl txffc
   抓取 DOM 完成，開始解析頁面
   時間 | 期號 | 開獎號
   20191103 04:51 | 0291 | 28348
   20191103 04:50 | 0290 | 26539
   20191103 04:49 | 0289 | 89468
   ... [以下省略]
   ```

### 二、 執行會處理 JS Render 的爬蟲
1. 安裝 Scrapy (已經安裝可跳過)
   - 先生成一個 python 2.7 的 Virtual Environment，例如 env_27
   - 安裝 scrapy
      - 參考: https://docs.scrapy.org/en/latest/intro/install.html
   ```bash
   (env_27) user$ pip install scrapy
   ```

2. 安裝 Docker  (已經安裝可跳過) (沒辦法，一時找不到不用 Docker 跑 Splash 的方法)
   - Ubuntu: 
   ```bash
   user$ sudo apt-get update && sudo apt install docker.io
   user$ sudo systemctl start docker
   ```
   - MacOS: [下載 dmg](https://download.docker.com/mac/stable/Docker.dmg) 或 homebrew
   ```bash
   user$ brew cask install docker
   ```

3. 安裝 splash docker 並啟動 splash server
   - 參考: https://splash.readthedocs.io/en/latest/install.html#ubuntu-12-04-manual-way
   ```bash
   user$ sudo docker pull scrapinghub/splash
   user$ sudo docker run -it -p 8050:8050 --rm scrapinghub/splash 
   ```
   - 說明： 他用 docker 封裝出一個 http server，提供 rendor js 的服務，當您啟動後，可嘗試 http://x.x.x.x:8050 存取頁面， x.x.x.x 是您跑 Splash Server 的主機 IP

4. 修改 settings.py，找到 SPLASH_URL 變數
   - 您的 spalsh Docker 跑在哪一台機器，IP 就改那一台機器。
   - 我把 spalsh 跑在 172.17.90.158:8050 ，所以設定為 
   ```python
   SPLASH_URL = 'http://172.17.90.158:8050'
   ```

5. 執行爬蟲 (Location: get_lottery_issue/get_lottery_issue/spiders/txffc_js.py)
   - 可以看到 data 已經是 js 執行後的結果，跟網頁最後看到的一致
   ```bash
   (env_27) user$ cd get_lottery_issue  # 第一層 get_lottery_issue
   (env_27) user$ scrapy crawl txffc_js
   時間 | 期號 | 開獎號
   20191103 18:16 | 1096 | 16157
   20191103 18:15 | 1095 | 35530
   20191103 18:14 | 1094 | 13465
   20191103 18:13 | 1093 | 63545
   20191103 18:12 | 1092 | 08404
   ... [以下省略]
   ```

### 三、 使用 Scrapy Console 從終端機進行檢測與開發
1. scrapy console 非常好用，可以在互動模式下，方便的去測試 Selector 該怎下
2. 下面簡單做個範例:
   2.1 進入 Shell
   ```bash
   (env_27) user$ scrapy shell http://www.tx-ffc.com/txffc
   ```
   2.2 複製貼上下面 Code 觀察結果(注意縮排XD)
   ```python
   issues = response.css("div.kj-info > div.kj-list > table > tbody > tr")
   for issue in issues:
      fields = issue.css("td")
      row_data = {}
      i = 1
      for field in fields:
         if i == 1:
            # 只 print 第一欄
            print( "DateTime: " + " ".join(field.css("td > font::text").extract()))
         i+=1
   ```
2.3 執行結果範例
   ```bash
   DateTime: 20191103 04:51
   DateTime: 20191103 04:50
   DateTime: 20191103 04:49
   DateTime: 20191103 04:48
   DateTime: 20191103 04:47
   ... [以下省略]
   ```

### 四、 執行爬蟲，並寫入 MySQL

1. 有先執行過上面 一 或 二，確定環境先 OK

2. 安裝 MySQLdb
   ```bash
   (env_27) user$ pip install MySQL-python
   ```

3. 啟動 MySQL 並建立 db 與 table 如下
   ```mysql
   CREATE DATABASE IF NOT EXISTS `scrapy_data` DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
   USE `scrapy_data`;
   CREATE TABLE `issue_data` (
      `id` INT(11) NOT NULL AUTO_INCREMENT,
      `datetime` VARCHAR(50) NULL DEFAULT NULL,
      `serial_no` VARCHAR(50) NULL DEFAULT NULL,
      `issue_no` VARCHAR(50) NULL DEFAULT NULL,
      `bigger_smaller_no` VARCHAR(50) NULL DEFAULT NULL,
      `odd_even_no` VARCHAR(50) NULL DEFAULT NULL,
      `sum_1` VARCHAR(50) NULL DEFAULT NULL,
      `sum_2` VARCHAR(50) NULL DEFAULT NULL,
      `sum_3` VARCHAR(50) NULL DEFAULT NULL,
      `dragon` VARCHAR(50) NULL DEFAULT NULL,
      `f3` VARCHAR(50) NULL DEFAULT NULL,
      `m3` VARCHAR(50) NULL DEFAULT NULL,
      `b3` VARCHAR(50) NULL DEFAULT NULL,
      PRIMARY KEY (`id`)
   )
   COLLATE='utf8mb4_unicode_ci'
   ENGINE=InnoDB;
   ```

4. 編輯  settings.py
   - 找到 ITEM_PIPELINES ，移除註解
   ```python
   ITEM_PIPELINES = {
       'get_lottery_issue.pipelines.GetLotteryIssuePipeline': 300,
   }
   ```

5. 編輯 settings.py 修改資料庫帳密
   ```python
   USERNAME = 'root'
   PASSWORD = '123'
   ```
   
6. 執行爬蟲 並查看資料庫寫入結果
   ```bash
   (env_27) user$ cd get_lottery_issue # 第一層 get_lottery_issue
   (env_27) user$ scrapy crawl txffc # 或 scrapy crawl txffc_js
    時間 | 期號 | 開獎號
   20191103 18:16 | 1096 | 16157
    - Saved
   20191103 18:15 | 1095 | 35530
    - Saved
   ... [以下省略]
   ```

## END
