class Hex:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.coordinates = (q, r)

    def __hash__(self):
        return int(self.coordinates)

    def __eq__(self, other):
        return other.coordinates == self.coordinates

    def __getitem__(self):
        return self.coordinates
