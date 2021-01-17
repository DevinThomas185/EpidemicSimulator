from random import randint, choice
from termcolor import colored
from state import State
from names import get_first_name, get_last_name
from random import randint, choice, choices


def get_death_probability(age):
    if age <= 19:
        return 0.002
    elif age <= 29:
        return 0.002
    elif age <= 39:
        return 0.002
    elif age <= 49:
        return 0.004
    elif age <= 59:
        return 0.013
    elif age <= 69:
        return 0.036
    elif age <= 79:
        return 0.080
    else:
        return 0.148


probability_of_wearing_mask = 0.9


def get_infection_probability(wears_mask):
    if wears_mask:
        return 0.1
    else:
        return 0.7


class Person:
    def __init__(self, start_x, start_y, id_number):
        self.id_number = id_number

        # Personal attributes
        self.gender = choice(["male", "female"])
        self.firstname = get_first_name(self.gender)
        self.surname = get_last_name()
        self.age = randint(18, 70)

        # Habitual attributes
        self.wears_mask = choices(population=[True, False],
                                  cum_weights=[probability_of_wearing_mask, 1 - probability_of_wearing_mask],
                                  k=1)[0]

        self.probability_of_infecting = get_infection_probability(
            self.wears_mask)  # TODO: Add variable infectivity depending on e.g maskwearer
        self.probability_of_death = get_death_probability(
            self.age)  # TODO: Add probability of death depending on gender

        # Position of person
        self.x = start_x
        self.y = start_y

        # Initial condition of person
        self.condition = State()

        self.generation_infected = None
        self.generation_immune = None

    def __repr__(self):
        return colored(self.firstname, self.condition.get_colour())

    # Required methods for a person
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def distance_to(self, neighbour):
        dx = (self.x - neighbour.x) ** 2
        dy = (self.y - neighbour.y) ** 2
        return (dx + dy) ** 0.5

    # Person methods to change the condition
    def infected(self, generation):
        if self.condition.state != "INFECTED":
            self.generation_infected = generation
            self.condition.becomes_infected()
            print(self.firstname, self.surname, "(ID:" + str(self.id_number) + ")", "has been infected in generation", str(generation)+".")

    def dies(self, generation):
        self.condition.dies()
        print(self.firstname, self.surname, "(ID:" + str(self.id_number) + ") has died, age", str(self.age) + ", in generation", str(generation)+".")

    def recover(self, generation):
        self.condition.recover()
        print(self.firstname, self.surname, "(ID:" + str(self.id_number) + ")" + ", age", str(self.age) + ", is now immune as of generation", str(generation)+".")

    # Boolean variables to test the state
    def is_infected(self):
        return self.condition.state == "INFECTED"

    def is_dead(self):
        return self.condition.state == "DEAD"

    def is_healthy(self):
        return self.condition.state == "HEALTHY"

    def is_immune(self):
        return self.condition.state == "IMMUNE"

    # Methods to infect or kill a person
    def maybe_infect(self, neighbour, generation):
        c = choices(population=["infect", "nothing"],
                    cum_weights=[self.probability_of_infecting, 1 - self.probability_of_infecting],
                    k=1)[0]
        if c == "infect":
            neighbour.infected(generation)  # Fine to infect both if one is already infected
            self.infected(generation)

    def maybe_die(self, generation):
        c = choices(population=["dies", "nothing"],
                    cum_weights=[self.probability_of_death, 1 - self.probability_of_death],
                    k=1)[0]
        if c == "dies":
            self.dies(generation)
