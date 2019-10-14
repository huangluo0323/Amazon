import requests
from lxml import etree
import csv


class Ymx:
    def __init__(self):
        self.url = 'https://www.amazon.cn/s?'
        # 'rh=n%3A831780051%2Cn%3A831784051&page=1&qid=1569634891&ref=lp_831784051_pg_2'
        # https://www.amazon.cn/s?rh=n%3A831780051%2Cn%3A831784051&page=1&qid=1569634891&ref=lp_831784051_pg_2
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'session-id=461-4965113-5747735; i18n-prefs=CNY; ubid-acbcn=462-1220067-3700430; x-wl-uid=1ezClfwXZq0dNn3aJT/R3GXDmeYJpH00RCl5SmeH2RePuWZ1bHuELl8GisJf7UP8M7FyXHeM/TSo=; lc-acbcn=zh_CN; amznacsleftnav-a4bf2096-6dde-3bcc-adfa-0cc8b22a7337=1,3,4; amznacsleftnav-4dde1384-ba1c-393c-afe9-48c1e4a02bf1=1; session-token=DuAtcApFYD3D8jddPQWn8Clu3JOFNacBI1bTTUdQSh41o88DF5y60c5BLA5n46JsQrEWBB/STE9HK12wnVUAx6P+SyHHRhqI8fISaZNi047oGptGxSaV7nhkC8MwoOgiGqRETFpTnuhPDTacPyephwU68IMLYYBDPh+d+TEE4xp69bbUBSFOGZo1Glun2zqO; session-id-time=2082787201l; csm-hit=tb:E6SH9JD0GRTXVK2Y15B2+s-JBPR6PH4B83EKR0H9T7W|1569644618244&t:1569644618244&adb:adblk_yes',
            # 'Host': 'www.amazon.cn',
            # 'Pragma': 'no-cache',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.page = 1
        self.csv = open('yamaxun.csv', 'a', encoding='utf-8-sig', newline='')
        self.filed = ['name', 'price']
        self.writer = csv.DictWriter(self.csv, self.filed)
        self.writer.writeheader()

    def jiexi(self, url):
        params = {'rh': 'n:831780051,n:831784051',
                  'page': self.page,
                  'qid': '1569634110',
                  'ref': 'lp_831784051_pg_2'}
        response = requests.get(url, headers=self.headers, params=params)
        html = etree.HTML(response.text)
        names_1 = html.xpath('.//div[@id="mainResults"]/ul/li/div/div[2]/div/div/a/img/@alt')
        names_2 = html.xpath('.//div[@class="s-result-list s-search-results sg-row"]'
                             '/div/div/span/div/div/div[2]/div/div/div/span/a/div/img/@alt')
        price_1 = html.xpath('.//div[@id="mainResults"]/ul/li/div/div[5]/div/a/span[2]/text()')

        price_2 = html.xpath('.//div[@class="s-result-list s-search-results sg-row"]'
                             '/div/div/span/div/div/div[2]/div[4]/div/div[1]/div/div/a/span/span[1]/text()')

        if names_1:
            names = names_1
        else:
            names = names_2
        if price_1:
            prices = price_1
        else:
            prices = price_2
        print(names)
        print(prices)
        next_url_1 = html.xpath('.//a[@title="下一页"]/@href')
        next_url_2 = html.xpath('.//li[@class="a-last"]/a/@href')

        for name, price in zip(names, prices):
            item = {}
            item['name'] = name
            item['price'] = price
            self.writer_csv(item)
        if next_url_1 or next_url_2:
            self.page += 1
            print(self.page)
            return self.jiexi(self.url)

    def writer_csv(self, item):
        self.writer.writerow(item)

    def run(self):
        self.jiexi(self.url)


if __name__ == '__main__':
    ya = Ymx()
    ya.run()
