import requests
from lxml import etree
import time
import random


def getBZ():
    url = 'https://wallhaven.cc/latest?page={}'

    # 翻页10页
    for page in range(1, 10):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        print(time.strftime("%H:%M:%S"))
        print("第{}页".format(page))

        url1 = url.format(page)
        print(url1)

        # 一级页面请求
        html = requests.get(url=url1, headers=headers).text
        data = etree.HTML(html)
        li_list = data.xpath('.//div[@id="thumbs"]//@href')

        for li in li_list:
            if 'latest' in li or 'top' in li:
                continue
            else:
                print(li)
                html_li = requests.get(url=li, headers=headers)
                print(html_li.status_code)

                if html_li.status_code == 404 or html_li.status_code == 429:
                    # 如果响应失败跳过这次数据抓取
                    continue
                else:
                    data = etree.HTML(html_li.text)
                    li_add = data.xpath('//*[@id="wallpaper"]//@src')
                    li_add = li_add[0]

                    # 区分横屏和竖屏壁纸
                    width = int(data.xpath('//*[@id="wallpaper"]//@data-wallpaper-width')[0])
                    height = int(data.xpath('//*[@id="wallpaper"]//@data-wallpaper-height')[0])

                    if width > height:
                        with open('landscape.txt', 'a', encoding='utf-8') as w:
                            w.write(li_add + '\n')
                    else:
                        with open('vertical.txt', 'a', encoding='utf-8') as w:
                            w.write(li_add + '\n')

                    b = random.randint(1, 2)
                    print("等待" + str(b) + "秒")
                    time.sleep(b)


getBZ()
