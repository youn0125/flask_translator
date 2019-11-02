"""
A simple bubble tea store flask app.
ata is stored in a SQLite database that looks something like the following:

+---------+-----------------+-----------+-------+---------+-------------+--------------+--------+---------------+---------+------------+
| Name    | Street          | City      | State | Zipcode | Store Hours | Phonenumber  | Rating | Menu          | Review  | signed_on  |
+=========+=================+===========+=======+=========+=============+==============+========+===============+=========+============+
| Bubble  |232 SW 122th Ave | Beaverton | OR    | 98006   | M-Sa: 10-9  | 503-232-1212 | 4      |Mango Bubble...| Awesome | 2012-05-28 |
+---------+-----------------+-----------+-------+---------+-------------+--------------+--------+---------------+---------+------------+

This can be created with the following SQL (see bottom of this file):

    create table bubbleteaStore (name text, staddr text, city text, state text, zipcode text, storehours text, phonenumber text,rating text, menu, review, signed_on date);

"""
from datetime import date
from .Model import Model
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
        Each row contains: name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review, date
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
        :param staddr: String
        :param city: String
        :param state: String
        :param zipcode: String
        :param storehours: String
        :param phonenumber: String
        :param rating: String
        :param menu: String
        :param review: String
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
