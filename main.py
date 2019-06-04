from cloudant.client import Cloudant


user = None
auth_token = None
db_url = "https://mikerhodes.cloudant.com"

# Note: login without credentials requires admin_party=True.
# This is not documented anywhere - found it in source, parent class, random docs
# https://guide.couchdb.org/draft/security.html
client = Cloudant(user, auth_token, admin_party=True, url=db_url, connect=True)

airportdb = client["airportdb"]
