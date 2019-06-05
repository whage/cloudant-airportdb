from math import radians, cos, sin, asin, sqrt
from cloudant.client import Cloudant
import json

user = None
auth_token = None
db_url = "https://mikerhodes.cloudant.com"

# Note: login without credentials requires admin_party=True.
# Couldn't find any documentation on this - found it in source, parent class, random docs
# https://guide.couchdb.org/draft/security.html
cloudant_client = Cloudant(user, auth_token, admin_party=True, url=db_url, connect=True)

class AirportDbClient():
    def __init__(self, cloudant_client):
        self.client = cloudant_client
        self.db = cloudant_client["airportdb"]

    #def get_airports_within_radius(lon1, lon2, lat1, lat2):
    def get_airports_within_radius(self, lat, lon, radius):
        # Note: implementing a half-solution for getting a bounding box:
        # treat world as if it was flat. Getting a bounding box for coordinates
        # around the poles seems really difficult.
        # We'll interpret radius as degrees.
        lon1 = max(-180, lon - radius)
        lon2 = min(180, lon + radius)
        lat1 = max(-90, lat - radius)
        lat2 = min(90, lat + radius)

        # Note: no need to sanitize input, the query will only read the db
        query = 'lon:[{} TO {}] AND lat:[{} TO {}]'.format(lon1, lon2, lat1, lat2)

        # No docs for this either, found by looking at source, searching for "search"
        airports = self.db.get_search_result("view1", "geo", q=query).get("rows", [])

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
            box_center_lon = (lon1 + lon2) / 2
            box_center_lat = (lat1 + lat2) / 2

            airport["distance"] = haversine(
                box_center_lon,
                box_center_lat,
                airport["fields"]["lon"],
                airport["fields"]["lat"]
            )

            return airport

        def get_distance(airport):
            return airport["distance"]

        airports_with_distance = list(map(add_distance, airports))
        airports_with_distance.sort(key=get_distance)

        return airports_with_distance


airport_db_client = AirportDbClient(cloudant_client)

print(json.dumps(airport_db_client.get_airports_within_radius(-20,-30, 20)))
