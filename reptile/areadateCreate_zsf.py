# -*- coding: utf-8 -*-
import pymysql
import csv

def school2area():
    # 先从数据库中获取所有学校信息
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                                   charset="utf8")
    cls = conn.cursor()
    sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
    cls.execute(sql1)
    results = cls.fetchall()
    # print(results)

    # 定义31个省市、澳门、香港、台湾
    provincestr = '''
    23个省分别为：河北省、山西省、辽宁省、吉林省、黑龙江省、江苏省、浙江省、安徽省、福建省、江西省、山东省、河南省、湖北省、湖南省、广东省、海南省、四川省、贵州省、云南省、陕西省、甘肃省、青海省、台湾省。
    5个自治区分别为：内蒙古自治区、广西壮族自治区、西藏自治区、宁夏回族自治区、新疆维吾尔自治区。
    4个直辖市分别为：北京市、上海市、天津市、重庆市。
    2个特别行政区分别为：香港特别行政区、澳门特别行政区。
    加上国外，共35类
    缺失：云南、贵州、青海、宁夏、广西
    
    '''
    school2prov_list = []
    for item in results:
        if item[0][0:2] in provincestr:
            school2prov_list.append([item[0], item[0][0:2]])
        else:
            school2prov_list.append([item[0], ' '])

    print(school2prov_list)

    # list存入csv
    with open('school2area.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in school2prov_list:
            writer.writerow(item)


# 读取school，area列表，生成以area为key的字典
def area2school():
    area_dict = {}
    # csv读如list
    data = []
    with open('school2area.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            data.append(item)
    # print(data)
    # 从data里提取数据，放入以area为key的字典
    for item in data:
        if item[1] in area_dict:
            area_dict[item[1]].append(item[0])
        else:
            area_dict[item[1]] = []
            area_dict[item[1]].append(item[0])
    # print(area_dict.keys(), len(area_dict.keys()))
    # 返回字典
    return area_dict

# 定义一个类，排序用
class scholar:
    def __init__(self, name, school, college, h, g, field, achievement_num):
        # 属性：姓名、学校、院系、h指数、g指数、领域、成果数
        self.name = name
        self.school = school
        self.college = college
        self.achi = achievement_num
        self.h = h
        self.g = g
        self.field = field


# 根据字典统计结果，统计并返回字典，key：省市名，value：该省前10热度学者
def scholarCntbyArea(area_dict):
    area_dict = dict(area_dict)
    # print(area_dict.keys())
    # 结果输出字典
    area_ans_dict = {}
    for area in area_dict.keys():  #
        # if area == '国外':
        #     continue
        # 为字典创建key
        area_ans_dict[area] = []
        scholar_list = []
        for school in area_dict[area]:
            # 创建数据库连接将该学校所有学者查询并放入scholar_list
            conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                                   charset="utf8")
            cls = conn.cursor()
            sql = "select name,school,college,Hpoint,Gpoint,field,achievement_num from %s where scholarid != '' ;" % school
            cls.execute(sql)
            conn.commit()
            results = cls.fetchall()
            # print('school:', school, results)
            conn.close()
            # 创建对象并放入scholar_list
            for per in results:
                try:
                    scholar_list.append(scholar(per[0], per[1], per[2], int(per[3]), int(per[4]), eval(per[5]), int(per[6])))
                except Exception as e:
                    print(e, '\nwrong: ', per[2], per[3])
        # 对当前地区所有学者排序
        scholar_list = sorted(scholar_list, key=lambda s: s.h+s.g, reverse=True)
        # 放入前10学者
        area_ans_dict[area].extend([[x.name, x.school, x.college, x.h, x.g, x.field, x.achi] for x in scholar_list[:10]])
        # print('area_ans_dict[%s]:' % area, area_ans_dict[area])
    return area_ans_dict

if __name__=='__main__':
    # area2school()
    area_scholar_dict = scholarCntbyArea(area2school())
    print(area_scholar_dict.keys())
    # 将生成的地区热度学者字典存入本地
    with open('area_scholar_dict.txt', 'w', newline='') as txtfile:
        txtfile.write(str(area_scholar_dict))
    print('---地区热度学者已存入本地---')
    # print('scholarCntbyArea：', scholarCntbyArea(area2school()))
    pass