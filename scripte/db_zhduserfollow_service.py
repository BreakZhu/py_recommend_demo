import csv
import pymysql
from DBUtils.PooledDB import PooledDB

# 打开数据库连接
url = "10.10.20.17"
host = 3506
uname = "mengdan"
upwd = "f+zuP$Q$iR0^*,uk"
db_name = "zhd_user_follow"
pool = PooledDB(pymysql, 5, host=url, user=uname, passwd=upwd, db=db_name, port=host, charset='utf8')


def get_user_follow_by_uid(table,uids):
    """
    :param uids:
    :return:
    """
    table_name = int(uids.split(",")[0]) % 100 + 1
    cursor, db = get_db_connector()
    sql = "SELECT follow_uid, followed_uid, follow_status FROM " \
          "follow_{} fll WHERE follow_uid in ({}) AND follow_status=2 ".format(table_name, uids)
    print(sql)
    try:
        cursor.execute('SET NAMES UTF8')
        cursor.execute(sql)  # 获取所有记录列表
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

with open('D:\\recommend_data\\user\\user.csv', 'r', encoding='utf-8') as csvfile:
    lines = csvfile.readlines()
    follow_file = open('D:\\recommend_data\\user\\user_follows.csv', 'a+', encoding='utf-8', newline='')
    writer = csv.writer(follow_file, dialect='excel')
    writer.writerow(['user', 'item', 'status'])
    numDict = dict()
    for user in lines[1:]:
        uid = int(user.split(",")[0])
        key = uid % 100 + 1
        uid = str(uid)
        if key not in numDict:
            ids = [uid]
            numDict[key] = ids
        else:
            ids = numDict.get(key)
            ids.append(uid)
            numDict[key] = ids

    for k, v in numDict.items():
        ids = ",".join(v)
        follow = get_user_follow_by_uid(k, ids)
        print('取出 {} 条关系记录'.format(len(follow)))
        writer.writerows(follow)
    follow_file.close()



