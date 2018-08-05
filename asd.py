import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.toutiao.com/a6585414038870557198/#p=2'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
}
response = requests.get(url, headers=headers)
#print(response.text)
soup = BeautifulSoup(response.text, 'lxml')
#print(soup)
pattern = re.compile('/(\d+)(.*?)","width":.*?"url_list":', re.S)
results = re.findall(pattern, response.text)
for result in results:
    #print(result[-1] + '\n')
    #print(type(result[-1]))
    #pattern1 = re.compile(r'pstatp.com\\/origin\\/pgc-image\\/(.*?)')
    #rs = re.search(pattern1, result[-1])

    m = result[-1].split('/')[-1]
    print(m)
    #print(rs)
#for m in result:
  #  print(m)
#image_url = 'http://p3.pstatp.com/origin/pgc-image/' + str(m)
#r = requests.get(image_url)
#with open('asd.jpg', 'wb') as f:
    #f.write(r.content)

#print(result.group(2))
#print(src)
#with open('sad.jpg', 'wb') as f:
    #f.write(response.content)