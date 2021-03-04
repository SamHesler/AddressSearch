import requests
import json

BASE = "http://127.0.0.1:5000/"
COUNTRIES = BASE + "countries"
ADDRESS_COMPONENTS = BASE + "addresscomponents/"
SEARCH_ADDRESS = BASE + "searchaddress"

responseCountries = requests.get(COUNTRIES)
responseCountries = responseCountries.json()
print("*** Call to get ***")
print("input: Nothing")
print("output: ", responseCountries)
print()
print()

# british virgin islands ([1]) is currently broken
input = responseCountries['countries'][2]
responseComponents = requests.post(ADDRESS_COMPONENTS + input)
responseComponents = responseComponents.json()
print("*** Call to post ***")
print("input: ", input)
print("output: ", responseComponents)
print()
print()


data = {'street' : '123 4th street', 'zip' : '76543', 'state' : 'Washington'}
responseSearch = requests.post(SEARCH_ADDRESS, data=data)
responseSearch = responseSearch.json()
print("*** Call to other post ***")
print("input: ", data)
print("output: ", responseSearch)
print()
print()