import mysql.connector

class Hippocampus:
    def __init__(self):
        self.cursor = self.connect_to_server()

    def connect_to_server(self):
        """Connects to the MySQL server and returns the cursor"""
        mydb = mysql.connector.connect(
            host="localhost",
            user="laptopadmin",
            password="SECRET",
            database="chatbot_memory"
        )
        return mydb.cursor()

    def find_entry(self, table, word):
        """Returns the primary key of the word in its table"""
        sql = "SELECT * FROM {} WHERE name='{}'".format(table, word)
        self.cursor.execute(sql)
        try:
            return list(self.cursor)[0][0]
        except IndexError:
            return None



    