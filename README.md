# 用途

定时查看amazonwarehouse二手的iphone 6plus列表,低于指定价格则发送邮件

# 使用

在amazon_iphone.py的sm函数中填写相应的邮箱信息,然后执行

 ```shell
 git clone https://github.com/dongzhuoyao/amazon_iphone
 cd amazon_iphone
 scrapy crawl amazon_iphone
 ```
 最后在新增一个crontab,每隔一个小时执行一次:
 执行 contab -e
 ```shell
0  * * * *  sh /path/to//scrapyTimer.sh
 ```

# 依赖

需要安装scrapy