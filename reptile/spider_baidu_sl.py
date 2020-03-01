from selenium.webdriver import Chrome,ChromeOptions
import time
import pymysql
option = ChromeOptions()  #创建配置实例
option.add_argument("--headless")  #在后台启动

conn = pymysql.connect(host="39.106.96.175",port=3306,db="scholar_info",user="root",password="12345678",charset="utf8")
cls = conn.cursor()
sql1="select table_name from information_schema.tables where table_schema='scholar_info'"   #获取当前所有表（学校）
cls.execute(sql1)
conn.commit()
results = cls.fetchall()
for i in results:
    sql2 = "select id,name,school from %s; " % (i)        #获取当前学校所有学者
    print(sql2)
    cls.execute(sql2)
    conn.commit()
    result = cls.fetchall()
    for j in result:
        print(j)
        name=j[1]
        school=j[2]
        url = "http://xueshu.baidu.com/usercenter/data/authorchannel?cmd=inject_page&author=%s&affiliate=%s"%(name,school)
        browser = Chrome(options=option)    #创建浏览器实例
        browser.get(url)                    #打开具体的网页
        all_a = browser.find_elements_by_css_selector("p.personInstitution")
        all_b = browser.find_elements_by_css_selector("a.searchResult_take")
        for i in range(0,len(all_a)):
            if school in all_a[i].text:
                print(all_a[i].text)
                print(all_b[i].get_attribute("href"))   #待爬取详细信息网址
        time.sleep(2)
        browser.quit()


