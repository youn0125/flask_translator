"""
A simple bubble tea stores flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from addstore import Addstore
from liststore import Liststore

app = flask.Flask(__name__)       # our Flask app

"""
Create the endpoint(index.html)
"""
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

"""
Creates the endpoint(addstore.html)
"""
app.add_url_rule('/addstore/',
                 view_func=Addstore.as_view('addstore'),
                 methods=['GET', 'POST'])

"""
Creates the endpoint(liststore.html)
"""
app.add_url_rule('/liststore/',
                 view_func=Liststore.as_view('liststore'),
                 methods=['GET'])

"""
local host port is 8000
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
