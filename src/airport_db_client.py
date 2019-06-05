from airport import Airport

class AirportDbClient():
    def __init__(self, cloudant_client):
        self.db = cloudant_client["airportdb"]

    def get_airports_within_radius(self, lat, lon, radius):
        # Note: implementing a half-solution for getting a bounding box:
        # treat world as if it was flat. Getting a bounding box for coordinates
        # around the poles seems really difficult.
        # We'll interpret radius as degrees.
        west = max(-180, lon - radius)
        east = min(180, lon + radius)
        south = max(-90, lat - radius)
        north = min(90, lat + radius)

        box_center = ((west + east) / 2, (south + north) / 2)

        # Note: no need to sanitize input, the query will only read the db
        query = 'lon:[{} TO {}] AND lat:[{} TO {}]'.format(west, east, south, north)

        # No docs for this either, found by looking at source, searching for "search"
        # TODO: find out how pagination works, currently `rows` contains max 25 elements
        airports_query_result = self.db.get_search_result("view1", "geo", q=query)
        rows = airports_query_result.get("rows", [])

        airports = list(map(lambda x: Airport(x, box_center), rows))
        airports.sort(key=lambda airport: airport.distance)

        return airports
