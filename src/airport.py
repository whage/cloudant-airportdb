from util import haversine

class Airport():
    def __init__(self, data, reference_point):
        self.name = data["fields"]["name"]
        self.lat = data["fields"]["lat"]
        self.lon = data["fields"]["lon"]

        self.distance = haversine(
            reference_point[0],
            reference_point[1],
            self.lon,
            self.lat
        )

    def __repr__(self):
        return "{}: {} km".format(self.name, self.distance)

    def __str__(self):
        return self.__repr__()
