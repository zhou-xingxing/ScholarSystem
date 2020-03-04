from selenium.webdriver import Chrome, ChromeOptions
import time
import pymysql
import spiderByUrl_zsf

option = ChromeOptions()  # 创建配置实例
option.add_argument("--headless")  # 在后台启动

#链接数据库遍历所有表
conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                       charset="utf8")
cls = conn.cursor()
sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
cls.execute(sql1)
conn.commit()
results = cls.fetchall()
for i in results:
    sql2 = "select id,name,school from %s; " % (i)  # 获取当前学校所有学者
    print(sql2)
    cls.execute(sql2)
    conn.commit()
    result = cls.fetchall()

    #对每一个学者去百度学术进行搜索
    for j in result:
        print(j)
        id = j[0]
        name = j[1]
        school = j[2]
        url = "http://xueshu.baidu.com/usercenter/data/authorchannel?cmd=inject_page&author=%s&affiliate=%s" % (
        name, school)
        browser = Chrome(options=option)  # 创建浏览器实例
        browser.get(url)  # 打开具体的网页
        all_a = browser.find_elements_by_css_selector("p.personInstitution")
        all_b = browser.find_elements_by_css_selector("a.searchResult_take")
        for k in range(0, len(all_a)):
            if school in all_a[k].text:
                print(all_a[k].text)
                print(all_b[k].get_attribute("href"))  # 待爬取详细信息网址
                # 使用option
                option = ChromeOptions()  # 创建配置示例
                option.add_argument('--headless')  # 无头模式，后台启动
                # 创建浏览器
                browser_baidu1 = Chrome(options=option)  # (options=option)
                browser_baidu2 = Chrome(options=option)
                Url = all_b[k].get_attribute("href")
                print('开始爬取')
                try:
                    info = spiderByUrl_zsf.spid(Url, browser_baidu1, browser_baidu2)    #调用爬取模块
                    # print('爬取完毕:\ninfo:\n', info)
                    sql2 = "UPDATE `scholar_info`.%s SET `scholarid` = '%s',`field`='%s', `cited_num`='%s', `achievement_num` = '%s', `Hpoint` = '%s', `Gpoint` = '%s', `achievement_list` = '%s', `achievement_list2` = '%s', `cited_list` ='%s', `partner_list` = '%s', `paper_name_list`='%s',`paper_info_list`='%s', `paper_search_list` ='%s',`collaborate_org` = '%s' WHERE `id` = %s; " % \
                           (school, info[0], str(info[1]).replace('\'','\\\''), str(info[2]).replace('\'','\\\''), str(info[3]).replace('\'','\\\''), str(info[4]).replace('\'','\\\''), str(info[5]).replace('\'','\\\''), str(info[6]).replace('\'','\\\''), str(info[7]).replace('\'','\\\''), str(info[8]).replace('\'','\\\''), str(info[9]).replace('\'','\\\''),
                            str(info[10]).replace('\'','\\\''), str(info[11]).replace('\'','\\\''), str(info[12]).replace('\'','\\\''),str(info[13]).replace('\'','\\\''),id)  # 获取当前学校所有学者
                    # print(sql2)
                    cls.execute(sql2)
                    conn.commit()
                except:
                    print(Url)
                browser_baidu1.quit()
                browser_baidu2.quit()
        time.sleep(2)
        browser.quit()
