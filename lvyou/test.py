# -*- coding: utf-8 -*-
import requests
import codecs


# url = "http://lvyou.baidu.com/jishou/jingdian/"
# url = "http://lvyou.baidu.com/business/advertisement/getadinfo?callback=jQuery18208650881557441181_1536718526406&industry=1&na_type=1&address_id=33&scene_id=751075a3a4c71261cb1fc3d9&_=1536718526507"
url = "https://lvyou.baidu.com/qianzhougucheng/remark/?rn=15&pn=0&style=hot#remark-container"
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.4.3000'
        }

def getHTMLText(url, headers):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常 "

def write2File(content,fileName,):
	"""
	将内容保存到指定路径的文件中
	"""
	fout=codecs.open(fileName,'w',encoding='utf-8')
	fout.write(content)
	fout.close()

if __name__ == '__main__':
    html = getHTMLText(url,headers)
    # print(html)
    write2File(html,"lvyou.txt")