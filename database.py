import sqlite3

class Database:
    def __init__(self):
        self.db = sqlite3.connect('slimy.db')
        self.create_classement_table()

    def create_classement_table(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        """)
        self.db.commit()

    def insertValues(self, name, score, date):
        sqlite_insert_query = """INSERT INTO classement (nom, score, date) 
                                 VALUES (?, ?, ?)"""
        val = (name, score, date)

        cursor = self.db.cursor()
        cursor.execute(sqlite_insert_query, val)

        self.db.commit()
        print(cursor.rowcount, "Successfully sent values to database")
        cursor.close()

    def getRankingFromDatabase(self):
        cursor = self.db.cursor()
        sqlite_select_query = """SELECT nom, max(score) FROM classement
                                 GROUP BY nom
                                 ORDER BY max(score) DESC
                                 LIMIT 4
                              """

        cursor.execute(sqlite_select_query)
        firstresult = cursor.fetchall()
        finalresult = []
        for r in firstresult:
            sqlite_date_query = """SELECT date FROM classement
                                   WHERE nom = ? AND score = ?
                                """
            cursor.execute(sqlite_date_query, (r[0], r[1]))
            result = cursor.fetchall()
            finalresult.append([r[0], r[1], result[0]])

        return finalresult
