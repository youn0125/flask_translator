"""
A simple bubble tea store flask app.
"""
from flask import Flask, redirect, request, url_for, render_template

#from model_sqlite3 import model
from model_pylist import model

app = Flask(__name__)       # our Flask app
model = model()

"""
Function decorator === app.route('/',index())
"""
@app.route('/')
@app.route('/index.html')
def index():
    """
    List bubble tea stores
    """
    entries = [dict(name=row[0], staddr=row[1], city=row[2], state=row[3], zipcode=row[4], storehours=row[5], phonenumber=row[6],
                    rating=row[7], menu=row[8], review=row[9], signed_on=row[10]) for row in model.select()]
    return render_template('index.html', entries=entries)

@app.route('/sign', methods=['POST'])
def sign():
    """
    Accepts POST requests, and processes the form;
    Redirect to index when completed.
    """
    model.insert(request.form['name'], request.form['staddr'], request.form['city'], request.form['state'],
                 request.form['zipcode'], request.form['storehours'], request.form['phonenumber'], request.form['rating'],
                 request.form['menu'], request.form['review'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
