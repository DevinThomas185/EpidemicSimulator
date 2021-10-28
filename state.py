colourMap = {"HEALTHY": "blue",
             "DEAD": "red",
             "INFECTED": "yellow",
             "IMMUNE": "white"}


class State:
    def __init__(self):
        self.state = "HEALTHY"
        self.is_healthy = True
        self.is_dead = False
        self.is_immune = False
        self.is_infected = False

    def becomes_infected(self):  # Healthy -> Infected
        self.state = "INFECTED"
        self.is_infected = True
        self.is_healthy = False
        self.is_dead = False
        self.is_immune = False

    def dies(self):  # Dies
        self.state = "DEAD"
        self.is_dead = True
        self.is_healthy = False
        self.is_immune = False
        self.is_infected = False

    def recover(self):  # Infected -> Immune
        self.state = "IMMUNE"
        self.is_immune = True
        self.is_infected = False
        self.is_healthy = False
        self.is_dead = False

    def immunity_wears(self):  # Immune -> Healthy
        self.state = "HEALTHY"
        self.is_healthy = True
        self.is_immune = False
        self.is_dead = False
        self.is_infected = False

    def get_colour(self):
        return colourMap[self.state]
