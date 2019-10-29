"""
A simple guestbook flask app.
ata is stored in a SQLite database that looks something like the following:

+------------+------------------+------------+----------------+
| Name       | Email            | signed_on  | message        |
+============+==================+============+----------------+
| John Doe   | jdoe@example.com | 2012-05-28 | Hello world    |
+------------+------------------+------------+----------------+

This can be created with the following SQL (see bottom of this file):

    create table guestbook (name text, email text, signed_on date, message);

"""
from datetime import date
from Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from bubbleteaStore")
        except sqlite3.OperationalError:
            cursor.execute("create table bubbleteaStore (name text, staddr text, city text, state text, zipcode text, storehours text, phonenumber text,rating text, menu, review, signed_on date)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: name, email, date, message
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bubbleteaStore")
        return cursor.fetchall()

    def insert(self, name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review):
        """
        Inserts entry into database
        :param name: String
        :param email: String
        :param message: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'name':name, 'staddr':staddr,'city':city, 
                'state':state, 'zipcode':zipcode, 'storehours':storehours, 'phonenumber':phonenumber, 
                'rating':rating, 'menu':menu, 'review':review, 'date':date.today()}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into bubbleteaStore (name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review, signed_on) VALUES (:name, :staddr, :city, :state, :zipcode, :storehours, :phonenumber, :rating, :menu, :review, :date)", params)

        connection.commit()
        cursor.close()
        return True
