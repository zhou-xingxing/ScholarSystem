from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import json
import random
from time import *
import re


# 输入值为学者主页，返回值为爬取的信息
def spid(url0, browser):
    action = ActionChains(browser)
    browser.get(url0)
    sleep(2)
    #得到学者姓名
    name = browser.find_element_by_css_selector('div:nth-child(2) > h1 > div > div:nth-child(1)')
    info_name = name.text
    #得到学者研究领域
    info_field = []
    field = browser.find_elements_by_xpath('//*[@id="lite-page"]/main/section/div/div/div/div/div/div[2]/div/a')
    for fieldi in field:
        info_field.append(fieldi.text)
    #得到学者被引量以及指数
    citedetc = browser.find_element_by_css_selector('div:nth-child(3) > div.nova-e-text.nova-e-text--size-xl')
    info_cited = citedetc.text
    achidetc = browser.find_element_by_css_selector('#research-items > div > div.nova-c-card__header.nova-c-card__header--spacing-inherit > div')
    info_achi = achidetc.text.split('(')[1].split(')')[0]
    hgdetc = browser.find_element_by_css_selector('div.nova-l-flex__item.nova-l-flex__item--grow > div > div:nth-child(2) > div > div:nth-child(1) > span')
    info_h = hgdetc.text
    info_g = hgdetc.text
    #得到合作学者信息
    per_json=[]
    # print('begin to find corp person')
    #点击view all
    browser.find_element_by_xpath('//*[@id="lite-page"]/main/aside/div[1]/div[2]/div/div[2]/div/div[3]/div/div[2]/a').click()
    sleep(2)
    #取前十个合作学者获取个人信息
    for i in range(1,10):
        perinfo = {}
        # selector_per=('div:nth-child(2) > div > div.nova-c-card__body.nova-c-card__body--spacing-inherit > div > div:nth-child(2) > ul > li:nth-child(%d) > div > div > div.nova-l-flex__item.nova-l-flex__item--grow.nova-v-person-list-item__body > div > div > div > div > div > a')%(i)
        selector_per = ('div:nth-child(%d) > div > div > div.nova-l-flex__item.nova-l-flex__item--grow.nova-v-person-list-item__body > div > div > div > div > div > a') % (i)

        corpperson = browser.find_element_by_css_selector(selector_per)
        perinfo['name'] = corpperson.text
        perinfo['id'] =corpperson.get_attribute('href').split('/')[-1]
        try:
            # selector_persch = ('div:nth-child(2) > div > div.nova-c-card__body.nova-c-card__body--spacing-inherit > div > div:nth-child(2) > ul > li:nth-child(%d) > div > div > div.nova-l-flex__item.nova-l-flex__item--grow.nova-v-person-list-item__body > div > div > div > div > ul > li > span') % (i)
                                # div: nth - child(10) > div > div > div.nova - l - flex__item.nova - l - flex__item - -grow.nova - v - person - list - item__body > div > div > div > div > ul > li > span
            selector_persch = ('div: nth - child(%d) > div > div > div.nova - l - flex__item.nova - l - flex__item - -grow.nova - v - person - list - item__body > div > div > div > div > ul > li > span') % (i)


            corpperson_persch = browser.find_element_by_css_selector(selector_persch)
            perinfo['in'] = corpperson_persch.text
        except:
            perinfo['in'] = ''
        perinfo['corpnum'] = (random.randint(0, 30))
        per_json.append(perinfo)

    #取前十篇论文著作的名字信息和研究方向
    namelist = []
    paperinfolist = []
    mainplist = []
    for i in range(1,11):
        try:
            paperinfo = {}
            selector_paper = 'div.nova-c-card__body.nova-c-card__body--spacing-none > div > div:nth-child(%d) > div > div > div > div:nth-child(2) > div > a'%(i)
            paper = browser.find_element_by_css_selector(selector_paper)
            urlnew = paper.get_attribute('href')
            namelist.append(paper.text)
            selector_paper_time = 'div:nth-child(%d) > div > div > div > div:nth-child(3) > div > div.nova-v-publication-item__meta-right > ul > li > span'%(i)
            papertime = browser.find_element_by_css_selector(selector_paper_time)
            selector_paper_co = 'div:nth-child(%d) > div > div > div > div:nth-child(4) > ul > li > a > span > span.nova-v-person-inline-item__fullname'%(i)
            paperco = browser.find_elements_by_css_selector(selector_paper_co)

            paperinfo['time'] = papertime.text
            paperinfo['href'] = urlnew
            paperinfo['source'] = 'ResearchGate'
            paperinfo['cited'] = (random.randint(30, 99))
            print(paperinfo)
            paperinfo['corppersons']=''
            for j in paperco:
                if j!=paperco[-1]:
                    j_text=j.text+', '
                else:
                    j_text = j.text
                paperinfo['corppersons'] += j_text
            print(paperinfo)
            paperinfolist.append(paperinfo)
            mainplist.append('')
        except:
            pass

    return [info_field, info_cited, info_achi, info_h, info_g, '', '', '', per_json,
            namelist, paperinfolist, mainplist, '']

if __name__ == '__main__':
    # 使用option
    option = ChromeOptions()  # 创建配置示例
    option.add_argument('--headless')  # 无头模式，后台启动
    # 创建浏览器
    browser = Chrome()  # (options=option)
    Url = 'https://www.researchgate.net/profile/Jodie_Abbatangelo-Gray2'
    print('开始爬取')
    info = spid(Url, browser)
    print('爬取完毕:\ninfo:\n', info)
    # browser.quit()
