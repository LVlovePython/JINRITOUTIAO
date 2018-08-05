#我的spider
import requests
from urllib.parse import urlencode
import time
from requests.exceptions import RequestException
from hashlib import md5
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool
import re

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
}

#根据自身需求改变爬取的数目
GROUP_START = 1
GROUP_END = 2


#此为获取街拍页
def get_page(offset):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except RequestException:
        print('请求索引出错')
        return None


#获取每个街拍描述详情页
def parse_page_index(json):
    data = json.get('data')
    if data:
        for item in data:
            article_url = item.get('article_url')
            url_numbers = int(item.get('gallary_image_count'))
            title = item.get('title')
            urls = []
            for num in range(1, url_numbers+1):
                url = str(article_url) + '#p=' + str(num)
                urls.append(url)
            yield {
                'image': urls,	#返回每张图片详情的url
                'title': title	#返回图集的title
            }


#通过正则表达式，回去图集中每张图片的url
def get_page_detail(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pattern = re.compile('/(\d+)(.*?)","width":.*?"url_list":', re.S)
            results = re.findall(pattern, response.text)
            images_url = []
            for result in results:
                end = result[-1].split('/')[-1]
                image_url = 'http://p3.pstatp.com/origin/pgc-image/' + str(end)
                images_url.append(image_url)
            return images_url
        else:
            return None
    except RequestException:
        print('请求详情页出错', url)
        return None


#保存图集中的每张图片并创建文件夹分类
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        for url in item['image']:
            image_url = get_page_detail(url)
            for img_url in image_url:
                response = requests.get(img_url, headers=headers)
                if response.status_code == 200:
                    file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
                    if not os.path.exists(file_path):
                        with open(file_path, 'wb')as f:
                            f.write(response.content)
                    else:
                        print('Already Downloaded', file_path)
                else:
                    return None
    except RequestException:
        print('Failed to save image')


#定义主函数
def main(offset):
    json = get_page(offset)
    for item in parse_page_index(json):
        save_image(item)
        print(item)


#调用主函数
if __name__ == '__main__':
    for i in range(GROUP_START, GROUP_END + 1):
        main(i*20)