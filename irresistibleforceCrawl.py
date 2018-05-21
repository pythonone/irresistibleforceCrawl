#this project is aimed to crawl interesting information for hacker
#-*- coding:utf-8 -*-
import requests
import datetime
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def crawlknowledgebefore(url):
    knowledgebeforelink=[]
    resp=requests.get(url)
    safesystem=re.findall("\[<i>.*?</i>\].*>",resp.content)
    for child in safesystem:
        child=child.replace("[<i> ","")
        child=child.replace(" </i>]  ",",")
        child = re.subn("<a href=.*?rel=\"nofollow\">", ",", child)
        child = child[0].replace("</a></p>", "")
        knowledgebeforelink.append(child)
    return knowledgebeforelink


def crawlknowledge(url):
    knowledgelink=[]
    resp=requests.get(url)
    safesystem=re.findall("<span class=\"category\">.*?</span>.*?<a href=.*?</a></p>",resp.content,re.S)
    if len(safesystem) is 0:
        knowledgelink=crawlknowledgebefore(url)
    for child in safesystem:
        child=child.replace("<span class=\"category\">[ ","")
        child=child.replace(" ]</span>  ",",")
        child=re.subn("<a href=.*?rel=\"nofollow\">",",",child)
        child=child[0].replace("</a></p>","")
        knowledgelink.append(child)
    return knowledgelink


def generaldate(start,end,step=1,format="%Y-%m-%d"):
    strptime,strftime=datetime.datetime.strptime,datetime.datetime.strftime
    days=(strptime(end,format)-strptime(start,format)).days
    return [strftime(strptime(start,format)+datetime.timedelta(i),format) for i in xrange(0,days,step)]

def main():

     
    errorurl=open('errorurl.txt','w')
    f=open('knowledge.txt','w')
    time=generaldate("2016-01-02", "2018-05-18")
    for day in time:
        day=day.replace("-","/")
        url='https://xuanwulab.github.io/cn/secnews/'+day+'/index.html'
        try:
            print day
            results = crawlknowledge(url)
            f.write(day)
            f.write('\n')
            for result in results:
                f.write(result)
                f.write('\n')
        except :
            print url

    errorurl.close()
    f.close()


if __name__=='__main__':
    main()

