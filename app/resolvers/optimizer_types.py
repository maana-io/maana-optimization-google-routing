
class Cargo:
    def __init__(self,
                 id=id,
                 origin=None,
                 dest=None,
                 volume=None,
                 weight=None,
                 laycanFrom=None,
                 laycanTo=None,
                 dischargeDateFrom=None,
                 dischargeDateTo=None,
                 revenue=0):
        self.id = id
        self.origin = origin
        self.destination = dest
        self.volume = volume
        self.weight = weight
        self.laycanFrom = laycanFrom
        self.laycanTo = laycanTo
        self.dischargeDateFrom = dischargeDateFrom
        self.dischargeDateTo = dischargeDateTo
        self.revenue = revenue
