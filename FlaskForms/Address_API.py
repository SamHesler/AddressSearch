from flask import Flask, request, render_template
from flask_restful import Api, Resource
import mysql.connector

app = Flask(__name__)
api = Api(app)

def dbConnection(command):
    db = mysql.connector.connect(user='API', password='HELL0IAMTH3API!',
                              host='127.0.0.1',
                              database='addresses')
    mycursor = db.cursor()
    if (type(command) is str):  
        mycursor.execute(command)
        return mycursor.fetchall()
    results = []
    for com in command:
        mycursor.execute(com)
        results.append(mycursor.fetchall())
    return results


class Countries(Resource):
    def get(self):
        countries = []
        #call to the database
        myresult = dbConnection("SHOW TABlES")
        for country in myresult:
            countries.append(country[0])
        countries.append("worldwide")
        #return to client
        return {'countries': countries}

class AddressComponents(Resource):
    def get(self, country):
        reply = []
        #call to the database to get a list of address components
        if country == "worldwide": #<- world wide search case
            commands = []
            allCountries = []
            tables = dbConnection("SHOW TABLES")
            for table in tables:
                allCountries.append(table[0])
            for c in allCountries:
                commands.append("SHOW COLUMNS FROM " + "`" + c + "`")
            result = dbConnection(commands)
            for res in result:
                for component in res:
                    if component[0] not in reply:
                        reply.append(component[0])
        else: #<- specific country search
            myresult = dbConnection("SHOW COLUMNS FROM " + "`" + country + "`")
            for x in myresult: 
                reply.append(x[0]) #<- this is just pulling the column names
        #return to client
        return {'address components': reply}

global LIMIT 
LIMIT = 50

class SearchAddress(Resource):
    def post(self):
        reply = {}
        searchCriteria = request.form.to_dict()
        #some call to the database to get a list of matching addresses
        if searchCriteria['country'] == "worldwide":  
            searchCriteria.pop('country')
            givenComponents = searchCriteria.keys()
            allCountries = []
            countriesToSearch = []

            
            commands = []
            tables = dbConnection("SHOW TABLES")
            for table in tables:
                allCountries.append(table[0])
            for country in allCountries:
                commands.append("SHOW COLUMNS FROM " + "`" + country + "`")
            results = dbConnection(commands)
            for count, res in enumerate(results):
                cleanCountryComponents = []
                for component in res:
                    cleanCountryComponents.append(component[0])
                if all(item in cleanCountryComponents for item in givenComponents):
                    countriesToSearch.append(allCountries[count])
            sqlCommandPart1 = "SELECT * FROM `"
            sqlCommandPart2 = "` WHERE "
            first = True
            for key in givenComponents:
                if not first:
                    sqlCommandPart2 = sqlCommandPart2 + " AND "
                sqlCommandPart2 = sqlCommandPart2 + key + " = '" + searchCriteria[key] +"'"
                first = False
            sqlCommandPart2 = sqlCommandPart2 + " LIMIT " + str(LIMIT)

            commands = []
            for country in countriesToSearch:
                commands.append(sqlCommandPart1 + country + sqlCommandPart2)
            results = dbConnection(commands)
            for count, result in enumerate(results):
                if result != []:
                    reply[countriesToSearch[count]] = result

        
        else:
            sqlCommand = "SELECT * FROM `" + searchCriteria["country"] + "` WHERE "
            first = True
            for key in searchCriteria.keys():
                if key != 'country':
                    if not first:
                        sqlCommand = sqlCommand + " AND "
                    sqlCommand = sqlCommand + key + " = '" + searchCriteria[key] +"'"
                    first = False
            sqlCommand = sqlCommand + " LIMIT " + str(LIMIT)
            reply[searchCriteria["country"]] = dbConnection(sqlCommand)
        return reply

api.add_resource(Countries, "/countries")
api.add_resource(AddressComponents, "/addresscomponents/<string:country>")
api.add_resource(SearchAddress, "/searchaddress")

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
