# 递归爬取，广度优先
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import json
from time import *
import re
import queue
import pymysql


# 设定起始url，李林的主页
# urlstart = 'http://xueshu.baidu.com/scholarID/CN-BK73256J'
# 建立待爬取的url队列
Info4srch = queue.Queue()
# 记录当前队列中出现过多少个网址
Cnt = 0

# 广度优先递归爬取，设定总爬取个数Nmax，起始url(默认为李林的主页)
# 这个数字为放入过url队列的个数，不一定都能爬下来：可能有重复、有非学校机构人员
def spid_breadth(Nmax = 10, urlstart = 'http://xueshu.baidu.com/scholarID/CN-BK73256J'):
    global Info4srch
    global Cnt
    # 初始化
    Info4srch.queue.clear()
    Cnt = 0
    # 将初始url放入队列
    Info4srch.put(urlstart)
    Cnt+=1

    # 使用option
    option = ChromeOptions()  # 创建配置示例
    option.add_argument('--headless')  # 在后台启动
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('blink-settings=imagesEnabled=false')
    option.add_argument('--disable-gpu')
    # 创建浏览器
    b1 = Chrome(executable_path="/home/scholar/Chrome/chromedriver",options=option)
    b2 = Chrome(executable_path="/home/scholar/Chrome/chromedriver",options=option)

    while (not Info4srch.empty()) :
        url = Info4srch.get()
        try:
            info = spid2(url, b1, b2, Nmax)
            print('爬取成功: ', url)
        except:
            print('爬取失败:', url)
            print('可能原因为该学者机构不能拆分成学校+学院的形式')
            continue
        # try:
        conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                               charset="utf8")
        cls = conn.cursor()
        # sql1是试图插入数据
        sql1 = "INSERT INTO `scholar_info`.`%s`(`name`, `school`, `college`, `scholarid`, `field`, `cited_num`, `achievement_num`, `Hpoint`, `Gpoint`, `achievement_list`, `achievement_list2`, `cited_list`, `partner_list`, `paper_name_list`, `paper_info_list`, `paper_search_list`, `collaborate_org`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); " % (
            str(info[14]), str(info[16]), str(info[14]), str(info[15]), info[0], str(info[1]).replace('\'', '\\\''), str(info[2]).replace('\'', '\\\''),
            str(info[3]).replace('\'', '\\\''), str(info[4]).replace('\'', '\\\''),
            str(info[5]).replace('\'', '\\\''), str(info[6]).replace('\'', '\\\''),
            str(info[7]).replace('\'', '\\\''), str(info[8]).replace('\'', '\\\''),
            str(info[9]).replace('\'', '\\\''),
            str(info[10]).replace('\'', '\\\''), str(info[11]).replace('\'', '\\\''),
            str(info[12]).replace('\'', '\\\''), str(info[13]).replace('\'', '\\\''))

        # sql2是试图刷新数据
        sql2 = "UPDATE `scholar_info`.%s SET `college` = '%s',`scholarid` = '%s',`field`='%s', `cited_num`='%s', `achievement_num` = '%s', `Hpoint` = '%s', `Gpoint` = '%s', `achievement_list` = '%s', `achievement_list2` = '%s', `cited_list` ='%s', `partner_list` = '%s', `paper_name_list`='%s',`paper_info_list`='%s', `paper_search_list` ='%s',`collaborate_org` = '%s' WHERE `name` = '%s'; " % \
               (str(info[14]), str(info[15]), info[0], str(info[1]).replace('\'', '\\\''), str(info[2]).replace('\'', '\\\''),
                str(info[3]).replace('\'', '\\\''), str(info[4]).replace('\'', '\\\''),
                str(info[5]).replace('\'', '\\\''), str(info[6]).replace('\'', '\\\''),
                str(info[7]).replace('\'', '\\\''), str(info[8]).replace('\'', '\\\''),
                str(info[9]).replace('\'', '\\\''),
                str(info[10]).replace('\'', '\\\''), str(info[11]).replace('\'', '\\\''),
                str(info[12]).replace('\'', '\\\''), str(info[13]).replace('\'', '\\\''), str(info[16]))  # 获取当前学校所有学者
        try:
            cls.execute(sql1)
            conn.commit()
            print('插入数据库成功')
            print('name:', info[16])
        except Exception as e:
            print('插入数据库失败的原因：', e)
            try:
                cls.execute(sql2)
                conn.commit()
                print('更新数据库成功')
                print('name:', info[16])
            except Exception as e2:
                print('更新数据库失败的原因:', e2)
                print('name:', info[16])

    b1.quit()
    b2.quit()
    sleep(0.5)


# 输入值为学者主页，最大队列url存在数，返回值为爬取的信息
def spid2(url0, browser, browser2, Nmax):
    global Info4srch
    global Cnt
    action = ActionChains(browser)
    try:
        browser.get(url0)
    except Exception as e:
        print(e)
    name = browser.find_element_by_css_selector('#author_intro_wr > div.person_baseinfo > div.p_name')
    info_name = name.text
    # print('info_name', info_name)
    inname = browser.find_element_by_xpath('//*[@id="author_intro_wr"]/div[2]/div[4]')
    info_in = inname.text

    # 拆分成学校和学院，如果拆分失败说明此主页非学校内学者
    info_school = info_in.split('大学')[0]+'大学'
    info_college = info_in.split('大学')[1]

    # print('info_in', info_in)
    id = browser.find_element_by_xpath('//*[@id="author_intro_wr"]/div[2]/div[3]/div')
    info_id = id.text.split(':')[-1]
    # print('info_id', info_id)
    field = browser.find_element_by_xpath('//*[@id="author_intro_wr"]/div[2]/div[6]/div/span[2]')
    info_field = field.text.split('/')
    # print('info_field', info_field)
    citedetc = browser.find_elements_by_css_selector('#author_intro_wr > div.person_baseinfo > ul > li> p.p_ach_num')
    info_cited = citedetc[0].text
    info_achi = citedetc[1].text
    info_h = citedetc[2].text
    info_g = citedetc[3].text
    # print('citedetc', info_cited, info_achi, info_h, info_g)
    # 定义一个字典作为成果列表
    achi_dict = {}

    try :

        browser.find_element_by_xpath('//*[@id="achievement_wr"]/div[1]/div[1]/div[4]/div').click()
        sleep(1)
        try:
            achi4 = browser.find_element_by_css_selector(
                '#achievement_wr > div.effectmap_pie > div.pieBox.otherBox > h3 > span.boxNumber'
                )
            achi_dict['其他'] = re.search('\(共(\d+?)篇\)', achi4.text).group(1)
        except Exception as e:
            # achi_list.append('0')
            pass
        #  焦点移动或者点击之后，一定要再把鼠标点回去
        # browser.find_element_by_css_selector('#author_intro_wr > div.person_image > a.person_portraitwr > img').click()
        # sleep(0.1)

        browser.find_element_by_xpath('//*[@id="achievement_wr"]/div[1]/div[1]/div[3]/div').click()
        sleep(1)
        try:
            achi3 = browser.find_element_by_css_selector(
                '#achievement_wr > div.effectmap_pie > div.pieBox.booktitleBox > h3 > span.boxNumber')
            achi_dict['专著'] = re.search('\(共(\d+?)篇\)', achi3.text).group(1)
        except Exception as e:
            pass
            # achi_list.append('0')
        # 焦点移动或者点击之后，一定要再把鼠标点回去
        # browser.find_element_by_css_selector('#author_intro_wr > div.person_image > a.person_portraitwr > img').click()
        # sleep(1)

        # 获取会议成果
        browser.find_element_by_xpath('//*[@id="achievement_wr"]/div[1]/div[1]/div[2]/div').click()
        sleep(1)

        try:
            achi2 = browser.find_element_by_css_selector(
                '#achievement_wr > div.effectmap_pie > div.pieBox.conferenceBox > p > span.boxnum')
            achi_dict['其他会议数'] = achi2.text
        except Exception as e:
            pass
            # achi_list.append('0')

        # 获取期刊成果
        browser.find_element_by_xpath('//*[@id="achievement_wr"]/div[1]/div[1]/div[1]/div').click()
        sleep(1)
        try:
            achi1s = browser.find_elements_by_css_selector(
                '#achievement_wr > div.effectmap_pie > div.pieBox.journalBox > p')
            for achi in achi1s:
                achi_dict[re.split('0|1|2|3|4|5|6|7|8|9', achi.text)[0]] = re.search('(\d+)', achi.text).group(1)
        except Exception as e:
            pass
                # print('no qikan')
    except Exception as e:
        print('No achis')


    # 定义一个json作为按年份统计的成果数
    tmptext = re.search('lineMapCitedData = (.*?);', browser.page_source)
    achi_json = tmptext.group(1)
    # print('achi_json', achi_json)

    # 定义一个json作为按年份统计的被引用数
    tmptext = re.search('lineMapAchData = (.*?);', browser.page_source)
    cited_json = tmptext.group(1)
    # print('cited_json', cited_json)

    # 点击合作学者的“更多”按钮（此处有“更多按钮”）
    per_json = []
    print('begin to find corp person')
    try:
        browser.find_element_by_css_selector('#main_content_right > div.co_author_wr > h3 > a').click()
        sleep(1)
        a1 = browser.find_element_by_css_selector('#co_rel_map > h3')
        corppersons = browser.find_elements_by_css_selector('#co_rel_map > div > a')
        # print('corppersons', corppersons)
        # print('num of corppersons', len(corppersons))
        # 定义json数组作为所有合作学者信息记录

        for corpperson in corppersons:
            urlnew = corpperson.get_attribute('href')
            # 如果数目没有超，则将urlnew放入队列
            if Cnt<Nmax:
                Info4srch.put(urlnew)
                Cnt+=1
            sleep(0.1)
            # 设置鼠标点击
            corpperson.click()
            # 定义json对象作为每个学者的个人信息记录
            perinfo = {}
            per = browser.find_elements_by_css_selector('#co_rel_map > div > div.co_relmap_tips > p')
            perinfo['name'] = per[0].text.split('：')[-1]
            perinfo['in'] = per[1].text.split('：')[-1]
            perinfo['corpnum'] = per[2].text.split('：')[-1]
            # 进入对应学者主页爬取scholarid

            browser2.get(urlnew)
            info_id2 = browser2.find_element_by_css_selector(
                '#author_intro_wr > div.person_baseinfo > div.p_scholarID > div')
            perinfo['id'] = info_id2.text.split(':')[-1]
            # 将个人信息填入合作学者信息集合
            per_json.append(perinfo)
            # 移回焦点
            browser.find_element_by_css_selector('#co_rel_map > a > i').click()
            browser.find_element_by_css_selector('#main_content_right > div.co_author_wr > h3 > a').click()
            # browser2.close()

    except Exception as e:
        print('没有“更多”按钮')
        corppersons = browser.find_elements_by_css_selector('#main_content_right > div.co_author_wr > div > div')
        urlnews = browser.find_elements_by_css_selector('#main_content_right > div.co_author_wr > div > div > a')
        for i in range(len(corppersons)):
            # main_content_right > div.co_author_wr > div > div > span > p:nth-child(1)
            # urlnew = corppersons[i].get_attribute('href')
            sleep(0.1)

            # 设置鼠标点击
            # corpperson.click()
            # 定义json对象作为每个学者的个人信息记录
            perinfo = {}
            perinfo['name'] = corppersons[i].text.split('\n')[0]
            perinfo['in'] = corppersons[i].text.split('\n')[1]
            # 如果没有合作次数，则全部写为1
            perinfo['corpnum'] = '1'
            # 如果数目没有超，则将urlnew放入队列
            if Cnt < Nmax:
                Info4srch.put(urlnews[i].get_attribute('href'))
                Cnt += 1
            # 进入对应学者主页爬取scholarid
            browser2.get(urlnews[i].get_attribute('href'))
            info_id2 = browser2.find_element_by_css_selector('#author_intro_wr > div.person_baseinfo > div.p_scholarID > div')
            perinfo['id'] = info_id2.text.split(':')[-1]

            # 将个人信息填入合作学者信息集合
            per_json.append(perinfo)

    # print('per_json', per_json)
    # 点击获取按照被引量降序的论文排列
    # 重新获取该网址

    print('begin to find paper')
    browser.get(url0)
    sleep(1)
    # 点击弹出按照被引排序的图表

    a1 = browser.find_element_by_css_selector(
        '#articlelist_container > div.in_content_rtop > div > div:nth-child(4) > div.time_sel_default.filter_sel_default'
    )
    action.move_to_element(a1).perform()

    sleep(1)

    # 点击按照被引排序按钮
    browser.find_element_by_css_selector(
        '#articlelist_container > div.in_content_rtop > div > div:nth-child(4) > div.time_filter_list.filter_list > ul > li:nth-child(2) > a'
    ).click()

    sleep(1)

    papers = browser.find_elements_by_css_selector(
        '#articlelist_container > div.in_content_result_wr > div.in_conternt_reslist > div> div.res_con > h3')

    namelist = []
    paperinfolist = []
    mainplist = []
    num = 10
    if len(papers) < num:
        num = len(papers)
    for i in range(num):
        paper = browser.find_element_by_css_selector(
            '#articlelist_container > div.in_content_result_wr > div.in_conternt_reslist > div:nth-child(' + str(
                i + 1) + ') > div.res_con > h3 > a')
        urlnew = paper.get_attribute('href')
        browser2.get(urlnew)
        namelist.append(browser2.find_element_by_css_selector('#dtl_l > div> h3').text)
        paperinfo = {}
        try:
            paperinfo['time'] = \
                browser2.find_element_by_css_selector(
                    '#dtl_l > div.main-info > div.c_content > div.year_wr').text.split('：')[
                    -1].replace('\n', '')
        except Exception as e:
            # print('no time')
            paperinfo['time'] = 'None'

        try:
            paperinfo['corppersons'] = browser.find_element_by_css_selector('#articlelist_container > div.in_content_result_wr > div.in_conternt_reslist > div:nth-child('+str(i+1)+') > div.res_con > div.res_info > span:nth-child(2)').text
        except Exception as e:
            paperinfo['corppersons'] = None
        try:
            citedsource = browser2.find_element_by_css_selector(
                '#dtl_l > div > div.c_content > div.ref_wr'
            ).text
            cited = re.search('(\d+)', citedsource).group(1)
            paperinfo['cited'] = cited
        except Exception as e:
            # print('no cited')
            paperinfo['cited'] = '0'

        infos = browser2.find_elements_by_css_selector('#dtl_r > div> div')
        for infoitem in infos:
            if '来源' in infoitem.text:
                paperinfo['source'] = browser2.find_element_by_css_selector(
                    '#dtl_r > div:nth-child(1) > div > div > div.container_right').text.replace('\n', ' ')
                # dtl_r > div:nth-child(1) > div > div > div.container_right
                break
        else:
            paperinfo['source'] = 'None'
        paperinfo['href'] = urlnew
        paperinfolist.append(paperinfo)

        for i in range(len(infos)):
            if '研究点分析' in infos[i].text:
                mainp = []
                mainps = browser2.find_elements_by_css_selector(
                    '#dtl_r > div:nth-child(' + str(i + 1) + ') > div > div > a')
                for s in mainps:
                    mainp.append(s.text[1:])
                break
        else:
            mainp = []

        mainplist.append(mainp)

    # print('namelist', namelist)
    # print('paperinfolist', paperinfolist)
    # print('mainplist', mainplist)
    corpins = browser.find_elements_by_css_selector('#main_content_right > div.co_affiliate_wr > ul > li')
    corpins_dict = {}
    for corpin in corpins:
        corpins_dict[corpin.text.split('\n')[0]] = corpin.text.split('\n')[1]


    return [info_id, info_field, info_cited, info_achi, info_h, info_g, achi_dict, achi_json, cited_json, per_json, namelist, \
           paperinfolist, mainplist, corpins_dict, info_school, info_college, info_name]


if __name__ == '__main__':
    spid_breadth()