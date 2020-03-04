#coding=utf-8
from selenium.webdriver import Chrome,ChromeOptions
import time
import pymysql
import importlib,sys
importlib.reload(sys)
#sys.setdefaultencoding('utf8')
option = ChromeOptions()  #创建配置实例
option.add_argument('--headless')  #在后台启动
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('blink-settings=imagesEnabled=false')
option.add_argument('--disable-gpu')

conn = pymysql.connect(host="39.106.96.175",port=3306,db="scholar_info",user="root",password="12345678",charset="utf8")
url = "https://www.mysupervisor.org/"
browser = Chrome(executable_path="/home/baize/Chrome/chromedriver",options=option)   #创建浏览器实例  executable_path="" options=option
browser.get(url)     #打开具体的网页
# html=browser.page_source  #获取页面源码
# print(html)
school = browser.find_elements_by_css_selector("li > dl > dt > div > a")

#找到所有学校元素进行遍历
for i in school:
    print(i.text)
    cls = conn.cursor()
    #按学校建表
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
          "`paper_info_list` text NULL,"\
          "`paper_search_list` varchar(2550) NULL," \
          "`collaborate_org` varchar(2550) NULL," \
          " PRIMARY KEY (`id`)" \
          ");" % (i.text)
    try:
        cls.execute(sql)
        conn.commit()
    except:
        continue
    schoolurl=i.get_attribute("href")
    schoolbrowser = Chrome(executable_path="/home/baize/Chrome/chromedriver",options=option)  # 创建浏览器实例  executable_path="" options=option
    schoolbrowser.get(schoolurl)  # 打开具体的网页
    # print(browser.find_elements_by_css_selector("li:nth-child(1) > dl > dt > div:nth-child(4) > a:nth-child(1)")[0].text)
    # browser.find_element_by_xpath('//*/li[1]/dl/dt/div[1]/a[1]').click()
    time.sleep(2)
    college=schoolbrowser.find_elements_by_css_selector("dl > dt > div > a")

    # 找到所有学院元素进行遍历
    for j in college:
        print(j.text)
        collegeurl = j.get_attribute("href")
        collegebrowser = Chrome(executable_path="/home/baize/Chrome/chromedriver",options=option)  # 创建浏览器实例  executable_path="" options=option
        collegebrowser.get(collegeurl)  # 打开具体的网页
        # childbrowser.find_element_by_xpath('//*/div[1]/div/ul[2]/li[1]/dl/dt/div/a').click()
        time.sleep(2)
        all_a = collegebrowser.find_elements_by_css_selector("a.topictitle")

        # 找到所有学者元素进行遍历
        for k in all_a:
            print(k.text)   #Webelement 对象.text 获取对象文本，.get_attribute（目标属性）
            cls = conn.cursor()
			#将学者的姓名学校和院系插入数据库
            sql = "INSERT INTO `scholar_info`.`%s`(`name`, `school`, `college`) VALUES ('%s', '%s', '%s'); " % (i.text,k.text,i.text,j.text)
            print(sql)
            cls.execute(sql)
            conn.commit()
        collegebrowser.quit()      #关闭浏览器
    schoolbrowser.quit()      #关闭浏览器
browser.quit()      #关闭浏览器
