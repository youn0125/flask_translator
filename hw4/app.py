"""
A simple bubble tea stores flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from addstore import Addstore
from liststore import Liststore

app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/addstore/',
                 view_func=Addstore.as_view('addstore'),
                 methods=['GET', 'POST'])

app.add_url_rule('/liststore/',
                 view_func=Liststore.as_view('liststore'),
                 methods=['GET'])


if __name__ == '__main__':	
    app.run(host='0.0.0.0', port=8000, debug=True)	# port number 8000
