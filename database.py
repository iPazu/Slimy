import mysql.connector

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
        host="51.210.96.48",
        user="root",
        passwd="slimydb",
        database="slimy")

    def insertValues(self):
        mySql_insert_query = """INSERT INTO classement (nom, score, date) 
                           VALUES 
                           ("Richard", 42, '05-06-2020') """

        cursor = self.db.cursor()
        cursor.execute(mySql_insert_query)
        self.db.commit()
        print(cursor.rowcount, "Successfully sent values to database")
        cursor.close()
    
    