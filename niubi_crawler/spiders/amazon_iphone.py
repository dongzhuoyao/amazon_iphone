# -*- coding: utf-8 -*-
import scrapy
import logging
import logging.handlers
from scrapy.selector import Selector
import smtplib
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


LOG_FILE = "amazon.log"
logger = logging.getLogger('amazon')
class AmazonIphoneSpider(scrapy.Spider):
    name = "amazon_iphone"
    allowed_domains = ["amazon.com"]
    start_urls = (
        'http://www.amazon.com/gp/offer-listing/B00NQHYWL2/ref=olp_twister_all?ie=UTF8&m=A2L77EE7U53NWQ&mv_color_name=all&mv_size_name=all',
    )

    def __init__(self,  *a,  **kwargs):
        super(AmazonIphoneSpider, self).__init__(*a, **kwargs)

        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info("amazon start..")

    def parse(self, response):
	logger.info("response success...")
        selector = Selector(response)
        iphone_lists = selector.xpath('//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()').extract()
        logger.info("result count: "+str(len(iphone_lists)))
        shouldEmail = False
        result = ''
	price_liststr = ''
        for iphone  in iphone_lists:
	    dollar_num = iphone.strip()
	    price_liststr = price_liststr+ ' '+dollar_num
            sixplus_price_num  = float(dollar_num[1:])
            if(sixplus_price_num<=500):
                shouldEmail = true
                result = str(sixplus_price_num)
            logger.info('price: '+str(sixplus_price_num))
        if(shouldEmail):
            self.sm('12345@qq.com','注意!目前有iphone6plus价格为'+result,'')
	else:
	    self.sm('12345@qq.com','amazon当前没有廉价iphone,价格为'+price_liststr,'')



    def sm(self,receiver, title, body):
            host = 'smtp.qq.com'
            port = 465
            sender = 'yourqqemail'
            pwd = 'yourqqemailsecuritypassword'#使用qq邮箱的安全密码

            msg = MIMEText(body, 'html')
            msg['subject'] = title
            msg['from'] = sender
            msg['to'] = receiver

            s = smtplib.SMTP_SSL(host, port)
            s.login(sender, pwd)
            s.sendmail(sender, receiver, msg.as_string())

            logger.info('The mail named %s to %s is sended successly.' % (title, receiver))
