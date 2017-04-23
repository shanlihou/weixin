#coding=utf8
import MySQLdb
import threading
from _mysql import OperationalError
Lock = threading.Lock()
class DBHelper(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(DBHelper, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
        
    def __init__(self):
        self.conn = MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'root', db = 'mysql')
        self.cur = self.conn.cursor()
        self.cur.execute("create table if not exists notify(id int NOT NULL AUTO_INCREMENT, time varchar(20), info varchar(50), type int, PRIMARY KEY (id))")
        self.cur.execute("create table if not exists filter(key_ varchar(20), value varchar(50), PRIMARY KEY (key_))")
        self.cur.execute("create table if not exists notify_all(id int NOT NULL AUTO_INCREMENT, wx_id varchar(40), date varchar(20), time varchar(20), info varchar(50), type varchar(8), PRIMARY KEY (id))")
        #type 0: times, 1: week or date, 2: reverse or not
        self.conn.commit()
        
    def insert(self, timeStr, info, tType=0):
        sql = 'insert notify(time, info, type) values(%s, %s, %s)'
        print type(tType)
        self.cur.execute(sql, (timeStr, info, tType))
        self.conn.commit()       
    def filtInsert(self, key, value):
        sql = 'insert filter(key_, value) values(%s, %s)'
        self.cur.execute(sql, (key, value))
        self.conn.commit()
    def allInsert(self, wx_id, date, time, info, type):
        sql = 'insert notify_all(wx_id, date, time, info, type) values(%s, %s, %s, %s, %s)'
        self.cur.execute(sql, (wx_id, date, time, info, type))
        self.conn.commit()       
        
        
    def query(self, timeStr):
        sql = 'select * from notify where time = %s'
        count = self.cur.execute(sql % (timeStr))
        result = self.cur.fetchmany(count)
        return result
    def filtQuery(self):
        sql = 'select * from filter'
        count = self.cur.execute(sql)
        result = self.cur.fetchmany(count)
        return result
    def allQuery(self, timeStr):
        sql = 'select * from notify_all where time = %s'
        count = self.cur.execute(sql % (timeStr))
        result = self.cur.fetchmany(count)
        return result
    
    def filtUpdate(self, key, value):
        sql = "update filter i set i.value = '%s' where i.key_ = '%s'"
        self.cur.execute(sql % (key, value))
        self.conn.commit()
        
    def delete(self, id):
        sql = 'delete from notify where id = %s'
        self.cur.execute(sql % (str(id)))
        self.conn.commit()
    def filtDelete(self, key):
        try:
            sql = 'delete from filter where key_ = %s'
            self.cur.execute(sql % (key))
            self.conn.commit()
        except OperationalError:
            print 'filtDelete'
    def allDelete(self, id):
        sql = 'delete from notify_all where id = %s'
        self.cur.execute(sql % (str(id)))
        self.conn.commit()
    
    def printDB(self, DBName):
        sql = 'select * from %s'
        count = self.cur.execute(sql % (DBName))
        result = self.cur.fetchmany(count)
        strRet = ''
        for i in result:
            for j in i:
	    	print j
                if type(j) != str:
                    strRet += str(j) + ' '
                else:
                    strRet += j.encode('utf8') + ' '
            strRet += '\n'
        return strRet
    def close(self):
        self.cur.close()
        self.conn.close()
