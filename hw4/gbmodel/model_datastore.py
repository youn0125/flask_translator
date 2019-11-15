# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Model import Model
from datetime import datetime
from google.cloud import datastore

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review, date]
    where name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu and review are Python strings
    and where date is a Python datetime
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['name'],entity['staddr'],entity['city'],entity['state'],entity['zipcode'],entity['storehours'],entity['phonenumber'],entity['rating'],entity['menu'],entity['review'],entity['date']]

class model(Model):
    def __init__(self):
        """
        Instantiate the client
        """
        self.client = datastore.Client('cs430-miyon-kim')

    def select(self):
        """
        Gets all entities(kind='store') from the datastore through from_datastore function
        Each row contains:name, staddr, city, state, zipcode, storehours, phonenumber, rating, menu, review, date
        :return: List of lists containing all rows from datastore
        """
        query = self.client.query(kind = 'Store')
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self,name,staddr,city,state,zipcode,storehours,phonenumber,rating,menu,review):
        """
        Put entry into datastore
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
        key = self.client.key('Store')
        store = datastore.Entity(key)
        store.update( {
            'name': name,
            'staddr': staddr,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'storehours': storehours,
            'phonenumber': phonenumber,
            'rating': rating,
            'menu': menu,
            'review': review,
            'date' : datetime.today(),
            })
        self.client.put(store)
        return True
