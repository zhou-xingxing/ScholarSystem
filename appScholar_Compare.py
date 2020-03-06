from flask import Flask, render_template, request,Blueprint
import pymysql
def compare(ScholarInfoLists,ScholarInfoIncluedeCollege,type):
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    scholarinfo = []
    need_part = '`name`,`scholarid`,`achievement_list`,`achievement_list2`,`cited_list`,`paper_search_list`'
    if type == 1:#合作学者无包含机构
        for scholar in ScholarInfoLists:
            name = scholar['name']
            id = scholar['id']
            school = str(scholar['in']).split('学')
            if len(school)>1:
                realschool = school[0]+'学'
            else:
                realschool = school[0]
            sql = "select %s from %s where id between 1 and 2500 and scholarid='%s'" % (need_part,realschool,id)
            print(sql)
            try:
                cls.execute(sql);
                conn.commit()
                result = cls.fetchall()
                if result:
                    scholarinfo.append(result)
            except:
                print('查询出错,无该学者所在学校或者表')
    elif type==2:#手动输入包含学院，但学院不是必填项
        for scholar in ScholarInfoIncluedeCollege:
            name = scholar['name']
            school = scholar['school']
            college = scholar['college']
            if college:
                sql = "select %s from %s where id between 1 and 2500 and name='%s' and colleg = '%s' " % (need_part,school,name,college)
            else:
                sql = "select %s from %s where id between 1 and 2500 and name='%s'" % (need_part, school, name)
            print(sql)
            try:
                cls.execute(sql);
                conn.commit()
                result = cls.fetchone()
                if result:
                    scholarinfo.append(result)
            except:
                print('查询出错,无该学者所在学校或者表')
    print(scholarinfo)
