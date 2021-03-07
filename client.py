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
print("output:")
for x in responseCountries['countries']:
    print("\t" + x)
print()
print()


input = responseCountries['countries'][12]
responseComponents = requests.post(ADDRESS_COMPONENTS + input)
responseComponents = responseComponents.json()
print("*** Call to post ***")
print("input: ", input)
print("output: ", responseComponents)
print()
print()


input = "worldwide"
responseComponents = requests.post(ADDRESS_COMPONENTS + input)
responseComponents = responseComponents.json()
print("*** Call to post ***")
print("input: ", input)
print("output: ", responseComponents['address components'])
print("output:")
for x in responseComponents['address components']:
    print("\t" + x)
print()
print()


#wordwide address search
data = {'country' : 'worldwide', 'street_number' : '2', 'postal_code' : '75243'}
responseSearch = requests.post(SEARCH_ADDRESS, data=data)
responseSearch = responseSearch.json()
print("*** Call to other post ***")
print("input: ", data)
print("output: ", responseSearch)
print("output: ")
for x in responseSearch:
    print(x,  responseSearch[x])
print()
print()

#country specific search
data = {'country' : 'australia', 'street_number' : '2'}
responseSearch = requests.post(SEARCH_ADDRESS, data=data)
responseSearch = responseSearch.json()
print("*** Call to other post ***")
print("input: ", data)
print("output: ", responseSearch)
print("output: ")
for x in responseSearch["australia"]:
    print(x)
print()
print()