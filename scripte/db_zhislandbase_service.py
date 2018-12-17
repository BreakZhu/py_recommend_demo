import csv
import pymysql
from DBUtils.PooledDB import PooledDB

# 打开数据库连接
url = "10.10.20.17"
host = 3506
uname = "mengdan"
upwd = "f+zuP$Q$iR0^*,uk"
db_name = "zhisland_base"
pool = PooledDB(pymysql, 5, host=url, user=uname, passwd=upwd, db=db_name, port=host, charset='utf8')


def get_users_by_page(start, pagesize):
    """
    :param page:
    :param pagesize:
    :return:
    """
    cursor, db = get_db_connector()
    # AND ub.base_rank = 400
    sql = "SELECT u.user_id, ub.default_user_com_id, ub.base_rank, ub.zhisland_type, ub.uname, " \
          "ub.country_code_show, ub.gender, ub.birthday, ub.id_type, ub.id_code,ub.org_province," \
          "ub.province, ub.city, ub.nationality, ub.wx_account, ub.industry, ub.industry_tag, " \
          "ub.recommend_total, ub.id_user_auth FROM user u LEFT JOIN user_base ub ON u.user_id = ub.user_id " \
          "WHERE u.activity=1 AND ub.base_rank IN (400,300) " \
          "ORDER BY u.user_id LIMIT {},{}".format(start, pagesize)
    try:
        # 执行SQL语句
        cursor.execute('SET NAMES UTF8')
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    db.close()
    return results


def get_db_connector():
    db = pool.connection()
    cursor = db.cursor()
    cursor.execute('SET NAMES UTF8')
    return cursor, db


"""
 
"""
with open('D:\\recommend_data\\user\\user.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(['user_id', 'default_user_com_id', 'base_rank', 'zhisland_type', 'uname',
                     'country_code_show', 'gender', 'birthday', 'id_type', 'id_code', 'org_province',
                     'province', 'city', 'nationality', 'wx_account', 'ub.industry', 'ub.industry_tag ',
                     'recommend_total', 'id_user_auth'])
    flag = True
    index = 0
    pagesize = 1000
    while flag:
        result = get_users_by_page(index, pagesize)
        print('取出 {} 条'.format(len(result)))
        writer.writerows(result)
        index += len(result)
        if len(result) == 0:
            flag = False
        print("写入csv文件 {} 行".format(index))
    csvfile.close()
