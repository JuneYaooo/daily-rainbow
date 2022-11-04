import pymysql
from sqlalchemy import create_engine
import re

class MySQL(object):
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def save_db(self, df, table):
        # 再插入新鲜的数据
        engine = create_engine(
            "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(self.user, self.passwd, self.host, self.port, self.db))
        df.to_sql(name=table, con=engine, if_exists='append', index=False, index_label=False)
        print('数据更新成功！')


    def table_exists(self, con, table_name):  # 这个函数用来判断表是否存在
        sql = "show tables;"
        tables = [con.execute(sql)]
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0  # 不存在返回0

    def exeSQL(self,sql):
        try:
            # 打开数据库连接
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                   database=self.db, charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = conn.cursor()
            print('数据库连接成功..')
            # 执行SQL语句
            cursor.execute(sql)
            result = cursor.fetchall()
            # 确认修改
            conn.commit()
            # 关闭游标
            cursor.close()
            # 关闭链接
            conn.close()
            print("语句 {} 执行成功！".format(sql))
            return result
        except Exception as e:
            print("语句 {} 执行失败！".format(sql))
            print('error!! ', e)
            return None

if __name__ == '__main__':
    db = MySQL()
    sql = "insert into suggestion(`id`,`wxid`,`type`,`raw_text`,`create_time`) values('SG20221023123550','wxid_ri2j0jsamq3l21','安利','安利缸子羊肉','2022-10-23 12:35:50');"
    print('sql',sql)
    res = db.exeSQL(sql)