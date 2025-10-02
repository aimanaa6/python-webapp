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
    # data access class with conn curser property
    # conn.close closes the connection
    def __del__(self):
        self.__conn.close()
    # added methods to be able to call SQL commands
    def query(self, command):
        self._cur.execute(command)
        return self._cur.fetchall()
    # fetchall grabs rows and returns them as a list of tuples
    def execute(self,command):
        self._cur.execute(command)
        # Get the last inserted ID
        # SELECT will return the rows requested
        # if running an inset/update/delete - execute change but don't commit yet
        inserted_id = self._cur.lastrowid
        self.__conn.commit()
        return inserted_id

