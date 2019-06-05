from math import radians, cos, sin, asin, sqrt
from cloudant.client import Cloudant
import json

user = None
auth_token = None
db_url = "https://mikerhodes.cloudant.com"

# Note: login without credentials requires admin_party=True.
# Couldn't find any documentation on this - found it in source, parent class, random docs
# https://guide.couchdb.org/draft/security.html
client = Cloudant(user, auth_token, admin_party=True, url=db_url, connect=True)

airportdb = client["airportdb"]

# TODO: read from user input
box_lon = (0, 10)
box_lat = (0, 10)

# note: no need to sanitize, the query will only read the db
query = 'lon:[{} TO {}] AND lat:[{} TO {}]'.format(box_lon[0], box_lon[1], box_lat[0], box_lat[1])

# No docs for this either, found by looking at source, searching for "search"
airports_within_bounds = airportdb.get_search_result("view1", "geo", q=query).get("rows", [])

# Spec states: "sorted by distance", doesn't state distance from where.
# We'll calculate distance from the center of the bounding box using the
# Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    earth_mean_radius = 6371

    # haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = earth_mean_radius
    return c * r

def add_distance(airport):
    box_center_lon = (box_lon[0] + box_lon[1]) / 2
    box_center_lat = (box_lat[0] + box_lat[1]) / 2

    airport["distance"] = haversine(
        box_center_lon,
        box_center_lat,
        airport["fields"]["lon"],
        airport["fields"]["lat"]
    )

    return airport

def get_distance(airport):
    return airport["distance"]

airports_with_distance = list(map(add_distance, airports_within_bounds))
airports_with_distance.sort(key=get_distance)

print(json.dumps(airports_with_distance))
