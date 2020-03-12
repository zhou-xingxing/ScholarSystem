from flask import Flask, render_template, request, Blueprint
import pymysql
import requests
import json
import time
import page_utils

app = Blueprint("appSearch_Result", __name__)


@app.route('/Search_result')
def appSearch_result():
    keyword = request.args.get('keyword')
    keyword2 = request.args.get('keyword2')
    keyword3 = request.args.get('keyword3')
    area_name = request.args.get('area_name')
    # scholarid=request.args.get('scholarid')
    search_type = request.args.get('type')
    if search_type != "8":
        start_time = time.time()  # 开始时间
        conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                               charset="utf8")
        cls = conn.cursor()
        sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
        cls.execute(sql1)
        conn.commit()
        results = cls.fetchall()
        # print(results)
        SQL = ""
        name = keyword
        need_part = '`id`,`name`,`school`,`college`,`field`,`achievement_num`'
        if search_type == "1":
            for i in results:
                sql = "select %s from %s where id between 1 and 2500 and name='%s'" % (need_part, i[0], name)
                if i != results[-1]:
                    sql += " UNION "
                SQL += sql
        elif search_type == "2":
            for i in results:
                sql = "select %s from %s where id between 1 and 2500 and college LIKE '%s'" % (
                need_part, i[0], '%' + name + '%')
                if i != results[-1]:
                    sql += " UNION "
                SQL += sql
        elif search_type == "3":
            sql = "select %s from %s where id between 1 and 2500" % (need_part, name)
            SQL += sql
        elif search_type == "4":
            for i in results:
                sql = "select %s from %s where id between 1 and 2500 and field LIKE '%s'" % (
                need_part, i[0], '%' + name + '%')
                if i != results[-1]:
                    sql += " UNION "
                SQL += sql
        elif search_type == "5":
            for i in results:
                sql = "select %s from %s where id between 1 and 2500 and scholarid='%s'" % (need_part, i[0], name)
                if i != results[-1]:
                    sql += " UNION "
                SQL += sql
            # return render_template('scholarinfo.html',result=result,length=length)
        # print(SQL+';')
        elif search_type == "6":  # 按论文搜索  3.6 bwm
            for i in results:
                sql = "select %s from %s where id between 1 and 2500 and paper_name_list LIKE '%s'" % (
                need_part, i[0], '%' + name + '%')
                if i != results[-1]:
                    sql += " UNION "
                SQL += sql
        elif search_type == "7":  # 高级搜索  3.6 bwm  3.12 sl
            for i in results:
                if (keyword2 != "" and keyword3 != ""):
                    sql = "select %s from %s where id between 1 and 2500 and name='%s' and school LIKE '%s' and college LIKE '%s'" % (
                    need_part, i[0], name, '%' + keyword2 + '%', '%' + keyword3 + '%')
                elif (keyword2 != "" and keyword3 == ""):
                    sql = "select %s from %s where id between 1 and 2500 and name='%s' and school LIKE '%s'" % (
                    need_part, i[0], name, '%' + keyword2 + '%')
                elif (keyword3 != "" and keyword2 == ""):
                    sql = "select %s from %s where id between 1 and 2500 and name='%s' and college LIKE '%s'" % (
                    need_part, i[0], name, '%' + keyword3 + '%')
                else:
                    sql = "select %s from %s where id between 1 and 2500 and name='%s'" % (need_part, i[0], name)
                if i != results[-1]:
                    sql += " UNION "
                SQL += sql
        try:
            cls.execute(SQL + ';')
            conn.commit()
            result = cls.fetchall()
            end_time = time.time()  # 结束时间
            print("time:", (end_time - start_time))  # 结束时间-开始时间
            length = len(result)
        except:
            result = []
            length = 0

    elif search_type == '8':
        # --地区热度学者推荐功能：type==8时，先从本地读入已经筛选过的模型，再处理并传回前端
        # http://baize.chinaeast.cloudapp.chinacloudapi.cn/Search_result?keyword=北京&type=8
        # dict_keys(['上海', '黑龙江', '辽宁', '吉林', '江苏', '湖南', '湖北', '北京', '山东', '安徽', '广东', '甘肃', '内蒙古', '天津', '江西', '福建', '台湾', '四川', '山西', '新疆', '河北', '浙江', '海南', '澳门', '陕西', '重庆', '西藏', '河南', '香港'])
        start_time = time.time()  # 开始时间

        with open('reptile\\area_scholar_dict.txt', 'r', newline='') as txtfile:
            area_scholar_dict = eval(txtfile.read())
        # 传给result列表
        result = []
        scholarlist = area_scholar_dict[keyword]
        length = len(scholarlist)
        for per in scholarlist:
            result.append([1, per[0], per[1], per[2], str(per[5]), per[6]])  # 添加一个“自增id属性”，为符合下面流程

    # 把研究领域的['','']去掉
    listresults = []
    for reone in result:
        if reone[4]:
            newstr = (reone[4].replace('[\'', ' ').replace('\']', ' ').replace('\', \'', ', '))
            newtuple = (reone[0], reone[1], reone[2], reone[3], newstr, reone[5])
        else:
            newtuple = (reone[0], reone[1], reone[2], reone[3], reone[4], reone[5])
        listresults.append(newtuple)
    end_time = time.time()  # 结束时间
    print("time:", (end_time - start_time))  # 结束时间-开始时间

    # 实现翻页
    li = []
    for i in range(1, length):
        li.append(i)
    pager_obj = page_utils.Pagination(request.args.get("page", 1), len(li), request.path, request.args,
                                      per_page_count=10)
    html = pager_obj.page_html()
    listresult = listresults[pager_obj.start:pager_obj.end]

    return render_template('search_result.html', result=listresult, length=length, html=html, keyword=keyword)
