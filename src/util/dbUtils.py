#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : dbUtils.py
# @Author: joker
# @Date  : 2018/11/11
# @Desc  :


import sqlite3
from util.tools import Tools


import pymysql
import hashlib
import time


class SqliteDbUtil(object):
    dbpath = Tools.resource_path("database.db")

    print("dbpath======%s" % dbpath)

    dbpath = 'C:\\Users\\user\\Desktop\\sales\\sales\\database.db'

    connect = sqlite3.connect(dbpath,check_same_thread=False)

    def __new__(self, *args, **kwargs):
        if not hasattr(self,'_instance'):
            self._instance = super().__new__(self)



    @staticmethod
    def select(sql):
        list =[]
        print(sql)
        try:
            c = SqliteDbUtil.connect.cursor()
            cursor = c.execute(sql)
            col_name_list = [tuple[0] for tuple in c.description]
            for row in cursor:
                # col_name_list
                dic = dict()
                i = 0
                while i < len(col_name_list):
                    dic[col_name_list[i]] = row[i]
                    i += 1
                list.append(dic)
                print(list)
        except Exception as e:
            print('发生错误')
        c.close()
        return list


    @staticmethod
    def DML(sql=None,values=None):
        print(sql)
        try:
            c = SqliteDbUtil.connect.cursor()
            c.execute(sql)
            SqliteDbUtil.connect.commit()
        except Exception as e:
            print("发生错误")
        finally:
            c.close()


    @staticmethod
    def sqlteTest():

        SqliteDbUtil.select("select f_name from wx_friend where host_name='192.168.1.2' and package_name='com.wHEID.multplugin03'")
        #
        # SqliteDbUtil.DML("update wx_equ set name = '657' where id = 0 ")
        #
        # SqliteDbUtil.DML("delete from wx_equ where id = 6 ")
        #
        # SqliteDbUtil.DML("insert into wx_package values(1,'微信 2', 'com.wHEID.multplugin04')")
        #
        # SqliteDbUtil.select("select id,name,ip from wx_equ")

class MysqlDbUtil(object):
    __db = None

    __cursor = None

    def __new__(self, *args, **kwargs):
        if not hasattr(self,'_instance'):
            self._instance = super().__new__(self)

            # 主机
            host = 'host' in kwargs and kwargs['host'] or 'localhost'

            # 端口
            port = 'port' in kwargs and kwargs['port'] or '3306'

            #用户名
            user = 'user' in kwargs and kwargs['user'] or 'root'

            # 密码
            password = 'password' in kwargs and kwargs['password'] or 'sghsse2007'

            # 数据库
            db = 'db' in kwargs and kwargs['db'] or 'wx_tools'

            # 编码
            charset = 'charset' in kwargs and kwargs['charset'] or 'utf8'

            # 打列数据库
            print('连接数据库')
            self.__db = pymysql.connect(host = host,port=int(port),user= user,password= password,db=db,charset= charset)

            # 创建一个游标对象
            self.__cursor = self.__db.cursor(cursor=pymysql.cursors.DictCursor)

        return self._instance

    # 返回执行语句后影响的行数
    def execute(self, sql):
        self.__cursor.execute(sql)
        rowcount = self.__cursor.rowcount
        return rowcount


    # 增->返回新增ID
    def insert(self,**kwargs):
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s set ' %table

        for k, v in kwargs.items():
            sql += "'%s'= '%s'" %(k,v)
        sql = sql.rstrip(',')

        print(sql)

        try:
            # 执行sql语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            # 获取自增ID
            res = self.__cursor.lastrowid
        except:
            self.__db.rollback()

        return res

    #  删除->返回影响的行数
    def delete(self,**kwargs):
        table = kwargs['table']
        where = kwargs['where']

        sql = 'DELETE FROM %s WHERE %s' %(table,where)
        print(sql)

        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            rowcount = self.__cursor.rowcount
        except:
            self.__db.rollback()

        return rowcount

    # 改-> 返回影响的行数
    def update(self,**kwargs):
        table = kwargs['table']
        kwargs.pop('table')

        where = kwargs['where']
        kwargs.pop('where')

        sql = 'update %s set' %table

        for k, v in kwargs.items():
            sql += "'%s' = '%s" %(k,v)
        sql = sql.rstrip(',')
        sql += ' where %s' %where

        print(sql)

        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            rowcount = self.__cursor.rowcount
        except:
            self.__db.rollback()

        return rowcount

    # 查->单条数据
    def fetchone(self,**kwargs):
        table = kwargs['table']

        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where' + kwargs['where'] or ''
        order =  'order' in kwargs and 'order by' +kwargs['order'] or ''
        sql = 'select %s from %s %s %s limit 1' %(field,table,where,order)
        print(sql)
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchone()
        except:
            self.__db.rollback()

        return data

    # 查-> 多条数据
    def fetchAll(self,**kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by' + kwargs['order'] or ''
        limit = 'limit' in kwargs and 'limit' + kwargs['limit'] or ''
        sql = 'select %s from %s %s %s %s' % (field, table, where, order, limit)
        print(sql)
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
        except:
            self.__db.rollback()

        return data
    #
    def __del__(self):
        self.__db.close()
        print('关闭数据库连接')

    def makeMd5(self,mstr):
        hmd5 = hashlib.md5()
        hmd5.update(mstr.encode('utf-8'))
        return hmd5.hexdigest()

    def getTime(self):
        return round(time.time())

    def timeFormat(self,timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    @staticmethod
    def testMySql():
        mySqldb = MysqlDbUtil(host='localhost', port=3306, user='root', password='sghsse2007', db='wx_tools',
                              charset='utf8')

        # 创建表
        print('创建表')
        sql = "DROP TABLE IF EXISTS `user`;"
        mySqldb.execute(sql)

        sql = '''
                   CREATE TABLE `user` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `name` varchar(50) NOT NULL,
                    `pwd` char(32) NOT NULL,
                    `insert_time` int(11) NOT NULL,
                     PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='用户表'; 
                '''
        print(sql)

        res = mySqldb.execute(sql)

        print(res)

        print('\n写入数据')





if __name__ == '__main__':

    SqliteDbUtil.sqlteTest()

    # MysqlDbUtil.testMySql()

