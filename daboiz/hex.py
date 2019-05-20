class Hex:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.coordinates = (q, r)

    def __hash__(self):
        return int(self.coordinates)

    def __eq__(self, other):
        return other.coordinates == self.coordinates

    def __getitem__(self, item):
        if item == "coordinates":
            return self.coordinates
        elif item == "q":
            return self.q
        elif item == "r":
            return self.r
        return 0
