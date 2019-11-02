from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        
                    
        entries = [dict(name=row[0], staddr=row[1], city=row[2], state=row[3], zipcode=row[4], storehours=row[5], phonenumber=row[6],
                    rating=row[7], menu=row[8], review=row[9], signed_on=row[10] ) for row in model.select()]
        return render_template('index.html',entries=entries)
