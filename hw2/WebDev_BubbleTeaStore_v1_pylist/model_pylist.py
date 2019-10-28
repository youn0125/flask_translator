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
        Returns guestentries list of lists
        Each list in guestentries contains: name, email, date, message
        :return: List of lists
        """
        return self.bubbleteaentries

    def insert(self, name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review):
        """
        Appends a new list of values representing new message into guestentries
        :param name: String
        :param email: String
        :param message: String
        :return: True
        """
        params = [name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review, date.today()]
        self.bubbleteaentries.append(params)
        return True
