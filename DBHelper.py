import MySQLdb
class DBHelper(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'root', db = 'mysql')
        self.cur = self.conn.cursor()
        self.cur.execute("create table if not exists notify(id int NOT NULL AUTO_INCREMENT, time varchar(20), info varchar(50), type int, PRIMARY KEY (id))")
        self.conn.commit()
    def insert(self, timeStr, info, tType=0):
        sql = 'insert notify(time, info, type) values(%s, %s, %s)'
        print type(tType)
        self.cur.execute(sql, (timeStr, info, tType))
        self.conn.commit()
    def query(self, timeStr):
        sql = 'select * from notify where time = %s'
        count = self.cur.execute(sql % (timeStr))
        result = self.cur.fetchmany(count)
        return result
    def delete(self, id):
        sql = 'delete from notify where id = %s'
        print type(id)
        self.cur.execute(sql % (str(id)))
        self.conn.commit()
    def close(self):
        self.cur.close()
        self.conn.close()