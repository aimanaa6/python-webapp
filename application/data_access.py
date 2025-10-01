import pymysql

class DataAccess:
    def __init__(self):
        self.__conn = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            db = "jokes"
        )
        self._cur = self.__conn.cursor()

    def __del__(self):
        self.__conn.close()

    def query(self, command):
        self._cur.execute(command)
        return self._cur.fetchall()

    def execute(self,command):
        self._cur.execute(command)
        self.__conn.commit()

