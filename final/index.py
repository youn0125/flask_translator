from flask import render_template
from flask.views import MethodView

from google.cloud import datastore
from google.cloud import storage

class Index(MethodView):
    def get(self):
        # Create a Cloud Datastore client.
    	datastore_client = datastore.Client()

    	# Use the Cloud Datastore client to fetch information from Datastore about
    	# each photo.
    	query = datastore_client.query(kind='Voices')
    	voice_entities = list(query.fetch())

        return render_template('index.html', voice_entities=voice_entities)