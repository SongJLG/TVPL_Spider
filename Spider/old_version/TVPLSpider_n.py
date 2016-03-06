# -*- coding: utf-8 -*-
from time import localtime
import urllib2
from bs4 import BeautifulSoup
import lxml

def st():
    print u"""
    #---------------------------------------
    #   写着玩儿，出问题概不负责，觉得方便，可以请我喝酒。
    #   请勿用于其他用途。
    #   Copyright Reserved by authors.
    #   1.0.1版本，可以直接在浏览器中调用脚本执行。还有一些其他改进。
    #   A spider for Catch TV Progam List.
    #   作者：老宋 平生多磨砺，男儿自横行。
    #   https://github.com/SongXX
    #   Date: 2015-12-30
    #---------------------------------------
    """
      
    print u"你可以在命令行后输入数字(1-6)来选择频道 "
    print u"通过在命令行后键入help获取频道列表"
    Select = str(raw_input())
    mySpider = TVPL_Spider(Select)
    mySpider.start()

class TVPL_Spider:
    def __init__(self, Select):
        self.channel = {"1":u"翡翠台", "2":u"明珠台", "3":u"国际台", "4":u"本港台", 
                       "5":u"凤凰卫视中文台", "6":u"澳亚卫视"}
                       
        self.ch_url = {"1":"TV_4/Channel_24", "2":"TV_4/Channel_25", "3":"TV_3/Channel_23", 
                        "4":"TV_3/Channel_22","5":"TV_5/Channel_26", "6":"TV_150/Channel_737"}
                        
        self.Select = Select
        
    def spider(self):
        for i in range(1,8):
            url = 'http://www.tvsou.com/program/'+ self.ch_url[self.Select] + '/W' + str(i) + '.htm'
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1;en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            r = urllib2.Request(url, headers = headers)
            content = urllib2.urlopen(r).read()
            soup = BeautifulSoup(content,"lxml")
            #tag = soup.find(attrs={"class":"tvgenre clear"})
            tags = soup.find(attrs={"class":"tvgenre clear"}).find_all("li")
            length = len(tags)
            print 'Day'+'%s' %i
            for j in range(length):
                print tags[j].text
            print ""    
        print u"爬虫抓取完成，不用谢。"
                                 
    def start(self):
        if self.Select == "help":
            for i in range(len(self.channel)):
                print "%3d : %3s" % (i+1, self.channel["%s" % (i+1)]),
            print ""
            st()

        elif self.Select not in self.channel.keys():
            print u"超出范围。请在1-6之间选择。"
            print ""
            st()
        
        else:
            print u"你选择了"+"%3s" %self.channel[self.Select]
            print u"正在获取节目单，请稍后..."
            print ""
            self.spider()