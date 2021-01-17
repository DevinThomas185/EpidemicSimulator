colourMap = {"HEALTHY": "blue",
             "DEAD": "red",
             "INFECTED": "yellow",
             "IMMUNE": "white"}


class State:
    def __init__(self):
        self.state = "HEALTHY"
        self.immune = False

    def dies(self):
        self.state = "DEAD"

    def becomes_infected(self):
        self.state = "INFECTED"

    def recover(self):
        self.state = "IMMUNE"
        self.immune = True

    def immunity_wears(self):
        self.immune = False

    def get_colour(self):
        return colourMap[self.state]
