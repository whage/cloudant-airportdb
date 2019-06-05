from cloudant.client import Cloudant


user = None
auth_token = None
db_url = "https://mikerhodes.cloudant.com"

# Note: login without credentials requires admin_party=True.
# Couldn't find any documentation on this - found it in source, parent class, random docs
# https://guide.couchdb.org/draft/security.html
client = Cloudant(user, auth_token, admin_party=True, url=db_url, connect=True)

airportdb = client["airportdb"]

#print("a0487237c4362b941f7332d7eb768ba0" in airportdb)


#for document in airportdb:
#    print(document)

#print(type(airportdb))

# No docs for this either, found by looking at source, searching for "search"
print(airportdb.get_search_result("view1", "geo", q="lon:[0 TO 30] AND lat:[0 TO 5]"))
