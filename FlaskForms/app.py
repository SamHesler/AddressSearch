from flask import Flask, render_template, request
from flask_restful import Api, Resource
import mysql.connector

app = Flask(__name__)
api = Api(app)

def dbConnection(command):
    db = mysql.connector.connect(user='API', password='HELL0IAMTH3API!',
                              host='127.0.0.1',
                              database='addresses')
    mycursor = db.cursor()
    mycursor.execute(command)
    return mycursor.fetchall()

# I commented out the database calls since the DB is local :)
class Countries(Resource):
    def get(self):
        countries = []
        #call to the database
        myresult = dbConnection("SHOW TABlES")
        for country in myresult:
           countries.append(country[0])
        #return to client
        return {"countries": countries}

class AddressCompoents(Resource):
    def get(self, country):
        reply = []
        #call to the database to get a list of address components
        myresult = dbConnection("SHOW COLUMNS FROM " + country)
        for x in myresult:
            print(x) 
            reply.append(x[0]) #<- this is just pulling the column names
        print(myresult)
        #return to client
        return {'address components': reply}
        #return '{"address components":["zip code", "street name", "postal code"]}'

class SearchAddress(Resource):
    def get(self):
        searchCriteria = request.form.to_dict()
        #some call to the database to get a list of matching addresses
        #return searchCriteria
        return ''

api.add_resource(Countries, "/countries")
api.add_resource(AddressCompoents, "/addresscomponents/<string:country>")
api.add_resource(SearchAddress, "/searchaddress")


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
