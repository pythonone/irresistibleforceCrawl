#this project is aimed to crawl interesting information for hacker
#-*- coding:utf-8 -*-
import requests
import datetime
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def crawlknowledge(url):
    knowledgelink=[]
    resp=requests.get(url)

    safesystem=re.findall("<div class=\"report-item\">.*?</a></div>",resp.content,re.S)
    for child in safesystem:
        child=child.replace("<div class=\"report-item\">","")
        child = child.replace("\n", "")
        child=child.replace("<div class=\"report-title\">","")
        child=child.replace("</div>                        ","")
        child=child.replace("                        ","")
        child=child.replace("<div class=\"report-link\"><a href=\"",",")
        child=re.subn("\" target=\"_blank\">.*?</div>","",child)
        try:

            title,realurl=child[0].split(",")
            respurl=requests.head(realurl)
            realurl=respurl.headers.get('location')
            child=title+","+str(realurl)

            knowledgelink.append(child)
        except:

            knowledgelink.append(child[0])
    return knowledgelink


def generaldate(start,end,step=1,format="%Y-%m-%d"):
    strptime,strftime=datetime.datetime.strptime,datetime.datetime.strftime
    days=(strptime(end,format)-strptime(start,format)).days
    return [strftime(strptime(start,format)+datetime.timedelta(i),format) for i in xrange(0,days,step)]

def main():

    errorurl=open('360error.txt','a')
    f=open('360daily.txt','a')
    time=generaldate("2018-03-30", "2018-06-07")
    for day in time:
        #day=day.replace("-","/")

        url='https://cert.360.cn/daily?date='+day
        results = crawlknowledge(url)

        f.write(day)
        f.write('\n')
        for result in results:
            f.write(result)
            f.write('\n')
        '''
        try:
            print day
            results = crawlknowledge(url)
            print type(results)
            f.write(day)
            f.write('\n')
            for result in results:
                f.write(result)
                f.write('\n')
        except :
            print url
        '''
    errorurl.close()
    f.close()


if __name__=='__main__':
    main()

