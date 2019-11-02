"""
Data is stored in a Python list.  Returns a list of lists
  upon retrieval
"""
from datetime import date
from Model import Model

class model(Model):
    def __init__(self):
        self.bubbleteaentries = []

    def select(self):
        """
        Returns bubble tea store entries list of lists
        Each list in bubble tea store entries contains: name, staddr, city, state, 
        zipcode, storehours, phonenumber, rating, menu, review
        :return: List of lists
        """
        return self.bubbleteaentries

    def insert(self, name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review):
        """
        Appends a new list of values representing new message into bubble tea store entries
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
        """
        params = [name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review, date.today()]
        self.bubbleteaentries.append(params)
        return True
