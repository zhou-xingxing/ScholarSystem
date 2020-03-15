from pypinyin import lazy_pinyin
import pymysql
import json

# 输入为名字汉字
# 输出为数据中可能出现的四种名字格式（列表）
def chinese2pinyin(str0):
    name_list = lazy_pinyin(str0)
    # print(name_list)
    name1 = str0
    name2 = ''.join(name_list[1:])+' '+name_list[0]
    name2 = name2.title()
    name3 = ''.join(name_list[1:]).title()+'-'+name_list[0].title()
    name4 = name_list[0]+' '+''.join(name_list[1:])
    name4 = name4.title()
    return [name1, name2, name3, name4]

# 传入为学者的姓名、学校名、
# 输出为学者的合作学者中和他存在论文（前十篇之内）合作关系的学者姓名、学者id列表
def corpbypaper(name, school):

    # 从数据库搜索该学者对应的信息
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    sql = "select partner_list,paper_info_list from %s where name='%s' " % (school, name)
    cls.execute(sql)
    result = cls.fetchone()
    # 将partner_list转化为列表形式
    try:
        partner_list = list(eval(result[0]))
    except:
        partner_list=[]
    # print('partner_list', partner_list)
    # print('paper_info_list(str)', result[1])
    corpbypaper_list = []
    for partner in partner_list:
        partner = dict(partner)
        try:
            name_guess_list = chinese2pinyin(partner['name'])
        except:
            print('汉字名字转化拼音时出错')
            continue
        # print(partner['name'], 'name_guess_list', name_guess_list)

        # 如果四种名字可能中存在一种在paper_info_list中存在，就将这位学者的名字和id填入输出列表
        if (name_guess_list[0] in result[1]) or (name_guess_list[1] in result[1]) or (name_guess_list[2] in result[1]) or (name_guess_list[3] in result[1]):
            # print('存在')
            corpbypaper_list.append(partner['name'])

    return corpbypaper_list


if __name__ == '__main__':

    str_name = input('输入学者名字:')
    str_id = input('输入学者学校：')
    print('在论文（前十篇之内）合作关系的学者为：\n', corpbypaper(str_name, str_id))
