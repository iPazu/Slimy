import mysql.connector

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
        host="51.210.96.48",
        user="root",
        passwd="slimydb",
        database="slimy")

    def insertValues(self,name,score,date):
        mySql_insert_query = """INSERT INTO classement (nom, score, date) 
                           VALUES (%s, %s, %s) """
        val = (name, score,date)

        cursor = self.db.cursor()
        cursor.execute(mySql_insert_query,val)

        self.db.commit()
        print(cursor.rowcount, "Successfully sent values to database")
        cursor.close()
    
    def getRankingFromDatabase(self):
        cursor = self.db.cursor()
        mySql_select_query = """SELECT nom,max(score) FROM classement
                           GROUP BY nom
                           ORDER BY max(score) DESC
                           LIMIT 4
                           """

        cursor.execute(mySql_select_query)
        firstresult = cursor.fetchall()
        finalresult = []
        for r in firstresult:
            sql_date_query = """SELECT date FROM classement
                                WHERE nom = "{}" AND score = {}
                                """.format(r[0],r[1])
            cursor.execute(sql_date_query)
            result = cursor.fetchall()
            finalresult.append([r[0],r[1],result[0]])


        return finalresult