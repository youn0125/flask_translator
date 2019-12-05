"""
A simple final project flask app.
"""

from flask import Flask, redirect, render_template, request

from index import Index

from google.cloud import datastore
from google.cloud import storage

CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

app = flask.Flask(__name__)       # our Flask app

"""
Create the endpoint(index.html)
"""
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

"""
Creates the endpoint(sayvoice.html)
"""
app.add_url_rule('/transvoice/',
                 view_func=Transvoice.as_view('index'),
                 methods=['GET', 'POST'])

"""
local host port is 8000
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
