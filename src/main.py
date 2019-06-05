import argparse
from cloudant.client import Cloudant
from airport_db_client import AirportDbClient

user = None
auth_token = None
db_url = "https://mikerhodes.cloudant.com"

# Note: login without credentials requires admin_party=True.
# Couldn't find any documentation on this - found it in source, parent class, random docs
# https://guide.couchdb.org/draft/security.html
cloudant_client = Cloudant(user, auth_token, admin_party=True, url=db_url, connect=True)
airport_db_client = AirportDbClient(cloudant_client)

title = 'Cloudant client demo'
parser = argparse.ArgumentParser(description = title)

parser.add_argument(
    'lat',
    type=float,
    help='Latitude of the POI',
)

parser.add_argument(
    'lon',
    type=float,
    help='Longitude of the POI',
)

parser.add_argument(
    'radius',
    type=float,
    help='Radius',
)

args = parser.parse_args()

print(airport_db_client.get_airports_within_radius(args.lat, args.lon, args.radius))
