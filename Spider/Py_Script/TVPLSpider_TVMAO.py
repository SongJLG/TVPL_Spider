# -*- coding: utf-8 -*-
from time import localtime
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
    #   2.0.0版本。大改动，爬取源更换成电视猫,同时利用模板直接生成Excel。
    #   如有建议，请发邮件 Sgang19890818@Gmail.com，或自行去GitHub修改源码。
    #   A spider for Catch TV Progam List.
    #   作者：老宋 平生多磨砺，男儿自横行。
    #   https://github.com/SongJLG/TVPL_Spider/
    #   Date: 2016-03-05
    #-------------------------------------------------------------------------
    """
    
    print u"你可以在命令行后输入数字(1-6)来选择频道"
    print u"通过在命令行后键入help获取频道列表"
    Select = str(raw_input())
    mySpider = TVPL_Spider(Select)
    mySpider.start()

class TVPL_Spider:
    def __init__(self, Select):
        self.channel = {"1":u"翡翠台", "2":u"明珠台", "3":u"国际台", "4":u"本港台",
                        "5":u"凤凰卫视中文台", "6":u"澳亚卫视"}                                          #需要爬取的电视台
                       
        self.ch_id = {"1":"TVB-TVB1", "2":"TVB-TVB2", "3":"HKATV-HKATV2",
                       "4":"HKATV-HKATV1", "5":"PHOENIX-PHOENIX1", "6":"MASTV-MASTV1"}                  #对应电视台的URL代码
        
        self.mould_xls = {"1":"TVB_FC_mould.xls", "2":"TVB_MZ_mould.xls", "3":"HKATV_GJ_mould.xls",
                          "4":"HKATV_BG_mould.xls", "5":"IFENG_WS_mould.xls", "6":"MASTV_AY_mould.xls"}     #对应的Excel模板
        
        self.Done_xls = {"1":"TVB_FC_Done.xls", "2":"TVB_MZ_Done.xls", "3":"HKATV_GJ_Done.xls", 
                          "4":"HKATV_BG_Done.xls", "5":"IFENG_WS_Done.xls", "6":"MASTV_AY_Done.xls"}        #对应的Excel完成文件
                          
        self.style_flag = 0             #Excle写入Style标记
        self.qula = 0                   #Excle写入数量统计
        self.Select = Select            
        
    def spider(self):
        old_wb = xlrd.open_workbook(self.mould_xls[self.Select], formatting_info = True)              #保留格式打开模板（貌似颜色被干掉，没保留）
        new_wb = copy(old_wb)                                                                         #复制一份模板
        new_ws = new_wb.get_sheet(0)
        style_0 = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue; font: bold on;')        #两种写入Style
        style_1 = xlwt.easyxf('font: bold on;')

        for i in range(7, 14):                                                          #由于电视猫周日只更新到下周六，所以爬取本周日为第一天，截止到下周六
            postdata = urllib.urlencode({ 'email':'786755516@qq.com', 'pwd':'1q2w3e', 'ek':'MTQ1NzE1ODM5OTEzMQ=='})    #模拟登陆，绕开电视猫的反爬虫机制
            url = 'http://www.tvmao.com/program_favorite/' + self.ch_id[self.Select] + '-w' + str(i) + '.html'
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1;en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  #伪装浏览器访问
            r = urllib2.Request(url, headers = headers, data = postdata)
            content = urllib2.urlopen(r).read()
            soup = BeautifulSoup(content,"lxml")
            tags = soup.find(attrs={"class": "epg mt10 mb10"}).find_all("li")
            length = len(tags)
    
            for j in range(length):                                                     #根据Style标记写入
                if self.style_flag == 0:
                    new_ws.write(j+self.qula+3, 1, tags[j].text, style_0)
                    self.style_flag = 1
        
                elif self.style_flag == 1:
                    new_ws.write(j+self.qula+3, 1, tags[j].text, style_1)
                    self.style_flag = 0
            
            self.qula += (length+4)       

        new_wb.save(self.Done_xls[self.Select])             #保存Excel文件
                
        print u"爬虫抓取完成"
                                 
    def start(self):
        if self.Select == "help":
            for i in range(len(self.channel)):
                print "%3d : %3s" % (i+1, self.channel["%s" % (i+1)])
            print ""
            st()     

        elif self.Select not in self.channel.keys():
            print u"超出范围。请在1-6之间选择。"
            print ""
            st() 
        
        else:
            print u"你选择了"+"%3s" %self.channel[self.Select]
            print u"正在获取节目单，请稍后..."
            self.spider()

if __name__=="__main__":
    st()
    