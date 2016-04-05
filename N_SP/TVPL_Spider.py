# -*- coding: utf-8 -*-
from datetime import *
import urllib
import urllib2
from bs4 import BeautifulSoup
import lxml
import xlrd
import xlwt
from xlutils.copy import copy

def st():
    print u"""
    #------------------------------------------------------------------------
    #   写着玩儿。请勿用于其他用途。如果觉得方便，可以请我喝酒。
    #   Copyright Reserved by authors.
    #   2.1.0版本。加入官网作为爬取源，EXCEL多页显示。不需要输入直接生成。
    #   请务必在周日使用，否则爬取内容会出错。请务必使PC本地日期正确。
    #   如有建议，请发邮件 Sgang19890818@Gmail.com，或自行去GitHub修改源码。
    #   A spider for Catch TV Progam List.
    #   作者：老宋 平生多磨砺，男儿自横行。
    #   https://github.com/SongJLG/TVPL_Spider/
    #   该版本发布 Date: 2016-04-05
    #-------------------------------------------------------------------------
    """
    
    old_wb = xlrd.open_workbook("TVPL_mould.xls", formatting_info = True)              #保留格式打开模板（貌似颜色被干掉，没保留）
    new_wb = copy(old_wb)                                                                         #复制一份模板
    
    for Select in range(1,5):
        Select = str(Select)
        mySpider = TVPL_Spider(Select, new_wb)
        mySpider.start()

    new_wb.save("TVPL_Done.xls")


class TVPL_Spider:
    def __init__(self, Select, new_wb):
        self.channel = {"1":u"翡翠台", "2":u"明珠台", "3":u"凤凰卫视中文台", "4":u"澳亚卫视"}                                          #需要爬取的电视台
                       
        self.ch_id = {"1":"TVB-TVB1", "2":"TVB-TVB2", "3":"PHOENIX-PHOENIX1", "4":"MASTV-MASTV1"}                  #对应电视台的URL代码
        
        self.style_flag = 0             #Excle写入Style标记
        self.qula = 0                   #Excle写入数量统计
        self.Select = Select
        self.new_wb = new_wb
        
        self.sheet_num = int(Select) -1
        self.style_0 = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue; font: bold on;')        #两种写入Style
        self.style_1 = xlwt.easyxf('font: bold on;')
        
    def spider_tvm(self):
        new_ws = self.new_wb.get_sheet(self.sheet_num)
        
        print u"正在获取节目单，请稍后..."

        for i in range(8, 15):
            postdata = urllib.urlencode({ 'email':'786755516@qq.com', 'pwd':'1q2w3e', 'ek':'MTQ1NzE1ODM5OTEzMQ=='})    
            url = 'http://www.tvmao.com/program_favorite/' + self.ch_id[self.Select] + '-w' + str(i) + '.html'
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1;en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  #伪装浏览器访问
            r = urllib2.Request(url, headers = headers, data = postdata)
            content = urllib2.urlopen(r).read()
            soup = BeautifulSoup(content,"lxml")
            tags = soup.find(attrs={"class": "epg mt10 mb10"}).find_all("li")
            length = len(tags)
    
            for j in range(length):                                                     #根据Style标记写入
                if self.style_flag == 0:
                    new_ws.write(j+self.qula+3, 1, tags[j].text, self.style_0)
                    self.style_flag = 1
        
                elif self.style_flag == 1:
                    new_ws.write(j+self.qula+3, 1, tags[j].text, self.style_1)
                    self.style_flag = 0
            
            self.qula += (length+4)
                           
        print u"爬虫抓取完成"
        print ""
        
    def spider_tvb(self):
        new_ws = self.new_wb.get_sheet(self.sheet_num)
        
        print u"正在获取节目单，请稍后..."
        
        if self.Select == "1":
            url = 'http://programme.tvb.com/jade/week/'
            
        elif self.Select == "2":
            url = 'http://programme.tvb.com/pearl/week/'
            
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1;en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = urllib2.Request(url, headers = headers)
        content = urllib2.urlopen(r).read()
        soup = BeautifulSoup(content, "lxml")
        today = date.today()
        
        for dm in range(1, 8):
            date_sel = today + timedelta(dm)
            rsl = soup.find(attrs={"id": "channellist"}).find_all(attrs={"date": date_sel})
            rsl_length = len(rsl)

            for i in range(rsl_length):
                tags = rsl[i].find_all("li")
                tags_length = len(tags)

                for j in range(tags_length):
                    if self.style_flag == 0:
                        new_ws.write(j+self.qula+3, 1, tags[j].text, self.style_0)
                        self.style_flag = 1

                    elif self.style_flag == 1:
                        new_ws.write(j+self.qula+3, 1, tags[j].text, self.style_1)
                        self.style_flag = 0

                self.qula += tags_length

            self.qula += 4
        
        print u"爬虫抓取完成"
        print ""
                            
    def start(self):
        if self.Select == "help":
            for i in range(len(self.channel)):
                print "%3d : %3s" % (i+1, self.channel["%s" % (i+1)])
            print ""
              

        elif self.Select not in self.channel.keys():
            print u"超出范围。请在1-4之间选择。"
            print ""
            
            
        elif self.Select == "1" or self.Select == "2":
            print u"你选择了"+"%3s" %self.channel[self.Select]
            self.spider_tvb()
            
        else:
            print u"你选择了"+"%3s" %self.channel[self.Select]
            self.spider_tvm()

if __name__=="__main__":
    print u'请确认今天是否是周日，如果是请输入小写：y。否则，请关闭，等待周日操作。'
    order = raw_input('Select Channel Num:')
    if order == "y":
        st()
   
      
    
        