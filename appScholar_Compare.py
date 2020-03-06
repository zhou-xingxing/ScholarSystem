from flask import Flask, render_template, request,Blueprint
import pymysql
def compare(ScholarInfoLists,ScholarInfoIncluedeCollege,type):
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    all_name = []
    achivement_list = []
    achivement_list2 = []
    citede_list =[]
    paper_search_list =[]
    need_part = '`name`,`scholarid`,`achievement_list`,`achievement_list2`,`cited_list`,`paper_search_list`'
    achiveminiyear,cited_minyear = 10000,10000;
    achivemaxyear ,cited_maxyear= 0,0
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
            #print(sql)
            try:
                cls.execute(sql);
                conn.commit()
                result = cls.fetchone()
                all_name.append(result[0])
                achivement_list.append(eval(result[2]))
                achivement_list2.append(eval(result[4]))
                citede_list.append(eval(result[3]))
                paper_search_list.append(eval(result[5]))
                citede_year = eval(result[3])
                achivement_year = eval(result[4])
                if int(citede_year[0]['year']) <cited_minyear:
                    cited_minyear = int(citede_year[0]['year'])
                if int(citede_year[len(citede_year)-1]['year']) > cited_maxyear:
                    cited_maxyear = int(citede_year[len(citede_year)-1]['year'])
                if int(achivement_year[0]['year']) < achiveminiyear:
                    achiveminiyear = int(achivement_year[0]['year'])
                if int(achivement_year[len(achivement_year)-1]['year']) > achivemaxyear:
                    achivemaxyear = int(achivement_year[len(achivement_year)-1]['year'])
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
                    all_name.append(name)
            except:
                print('查询出错,无该学者所在学校或者表')

    # print(all_name)
    # print(achivement_list)
    # print(achivement_list2)
    # print(citede_list)
    # print(paper_search_list)
    # print(achiveminiyear)
    # print(achivemaxyear)
    # print(cited_minyear)
    # print(cited_maxyear)