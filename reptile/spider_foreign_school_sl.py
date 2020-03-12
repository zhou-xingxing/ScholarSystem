from selenium.webdriver import Chrome, ChromeOptions
import time
import pymysql
import sys
import spider_foreign_sl
from time import *

option = ChromeOptions()  # 创建配置实例
option.add_argument('--headless')  #在后台启动
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('blink-settings=imagesEnabled=false')
option.add_argument('--disable-gpu')

# 创建浏览器
schoolbrowser = Chrome(executable_path="/home/baize/Chrome/chromedriver",options=option)  # (options=option)
#给出待爬取的学校url
schoolUrl = 'https://www.researchgate.net/institution/University_of_Chicago/departments'
schoolbrowser.get(schoolUrl)  # 打开具体的网页
sleep(2)
#链接数据库
conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
cls = conn.cursor()
schoolget=schoolUrl.split("/")[-2].replace('%20','_')
# 按学校建表
sql = "CREATE TABLE `scholar_info`.`%s`  (" \
      "`id` int(0) NOT NULL AUTO_INCREMENT," \
      "`name` varchar(255) NOT NULL," \
      "`school` varchar(255) NOT NULL," \
      "`college` varchar(255) NOT NULL," \
      "`scholarid` varchar(255) NULL," \
      "`field` varchar(255) NULL ," \
      "`cited_num` varchar(10) NULL," \
      "`achievement_num` varchar(10) NULL," \
      "`Hpoint` varchar(10) NULL ," \
      "`Gpoint` varchar(10) NULL," \
      "`achievement_list` varchar(2550) NULL," \
      "`achievement_list2` varchar(2550) NULL," \
      "`cited_list` varchar(2550) NULL," \
      "`partner_list` varchar(2550) NULL," \
      "`paper_name_list` varchar(2550) NULL," \
      "`paper_info_list` text NULL," \
      "`paper_search_list` varchar(2550) NULL," \
      "`collaborate_org` varchar(2550) NULL," \
      " PRIMARY KEY (`id`)" \
      ");" % (schoolget)
try:
    cls.execute(sql)
    conn.commit()
except:
    pass

#遍历该学校全部院系url
college= schoolbrowser.find_elements_by_css_selector("div > div.name > a > span")
for collegei in college:
    collegetxt = collegei.text
    collegeurl='https://www.researchgate.net/institution/%s/department/%s/members'%(schoolget,collegei.text)
    print(collegetxt,collegeurl)
    collegebrowser = Chrome(executable_path="/home/baize/Chrome/chromedriver",options=option)  # (options=option)
    # scholarbrowser = Chrome()  # (options=option)
    collegebrowser.get(collegeurl)  # 打开具体的网页
    sleep(2)
    # 遍历该院系全部成员url
    members = collegebrowser.find_elements_by_css_selector("div.indent-content > h5 > a")
    for member in members:
        membertxt = member.text
        memberurl = member.get_attribute('href')
        print(membertxt, memberurl)
        scholarname=membertxt
        school=schoolget
        college=collegei.text
        scholarid=memberurl.split('/')[-1]
        scholarbrowser = Chrome(executable_path="/home/baize/Chrome/chromedriver",options=option)  # (options=option)
        sleep(2)
        try:
            info = spider_foreign_sl.spid(memberurl, scholarbrowser)    #调用爬取学者信息模块
            #print('爬取完毕:\ninfo:\n', info)
            #将返回信息插入数据库
            conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
               charset="utf8")
            cls = conn.cursor()
            sql2 = "INSERT INTO `scholar_info`.`%s`(`name`, `school`, `college`, `scholarid`,`field`,`cited_num`, `achievement_num`, `Hpoint`, `Gpoint`, `achievement_list`,`achievement_list2`, `cited_list`, `partner_list`,`paper_name_list`,`paper_info_list`, `paper_search_list`,`collaborate_org`) VALUES ('%s','%s', '%s','%s','%s', '%s','%s','%s', '%s','%s', '%s','%s','%s', '%s','%s','%s', '%s'); " % \
                   (schoolget,scholarname,school, college, scholarid,str(info[0]).replace('\'','\\\''),info[1] ,info[2] ,info[3], info[4], '', '', '',str(info[8]).replace('\'','\\\''), str(info[9]).replace('\'','\\\''),
                    str(info[10]).replace('\'','\\\''),  '', '')  # 获取当前学校所有学者
            print(sql2)
            cls.execute(sql2)
            conn.commit()
        except Exception as e:
            print(e)
        scholarbrowser.quit()
    collegebrowser.quit()
schoolbrowser.quit()
