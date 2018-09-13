import requests
from lxml import etree
import lxml
import pandas as pd
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Host": "lvyou.baidu.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"
}
place=['qianzhougucheng']
for name in place:
    s=[]
    score=[]
    for i in range(0,100,15):    # 点评数
        url="https://lvyou.baidu.com/%s/remark/?rn=15&pn=%d&style=hot#remark-container" %(name,i)
        print ("url=",url)
        print ('i=',i)
        try :
            html=requests.get(url,headers=headers)
        except :
            pass
        else:
            # print ("html=",html)
            if str(html)=="<Response [200]>":
                # print (html)
                html.encoding="utf-8"
                selecter=etree.HTML(html.text)
                # pinglun=selecter.xpath("""normalize-space(//*[@id="remark-container"]/div[3]/div/div[2]/div[2]/div[1]/text())""")
                # etree.tostring(pinglun[0],print_pretty=True, method='html')
                for j in range(1,16):
                    numsum=selecter.xpath("""//*[@id="remark-container"]/div[1]/span/text()""")
                    print("评论数")
                    print(numsum[0])  # 评论数

                    group = re.findall(r"\d{1,2}",numsum[0])
                    remark_acccount = group[0]
                    print(remark_acccount)

                    # if i > int(remark_acccount):
                    #     break

                    p=selecter.xpath("""//*[@id="remark-container"]/div[3]/div[%d]/div[2]/div[2]/div[1]/node()"""%j)
                    try :
                        c=selecter.xpath("""//*[@id="remark-container"]/div[3]/div[%d]/div[2]/div[1]/div[1]/div/@class"""%j)
                        # print (c)
                        c=c[0][-1]
                    except IndexError:
                        pass
                    # print (j)
                    st=""
                    for i in p:
                        # print ("p=",p)
                        if type(i)==lxml.etree._Element:
                            i=i.text
                        try:
                            st=st+i
                        except TypeError:
                            pass
                    s.append(st)
                    score.append(c)
                    print ("st=",st)

            else:
                print ("url is unable")
                pass
        while '' in s:
            s.remove('')

    info = {}
    info['scene_name'] = name
    info['pinglun'] = s
    info["start"]=score[:len(s)]
    # print(info)