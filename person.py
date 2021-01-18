from termcolor import colored
from state import State
from names import get_first_name, get_last_name
from random import randint, choice, choices
import variables


def print_if(to_print, statement):
    if to_print:
        print(statement)


def get_death_probability(age):
    if age < 20:
        return variables.death_less_than_20
    elif age < 30:
        return variables.death_less_than_30
    elif age < 40:
        return variables.death_less_than_40
    elif age < 50:
        return variables.death_less_than_50
    elif age < 60:
        return variables.death_less_than_60
    elif age < 70:
        return variables.death_less_than_70
    elif age < 80:
        return variables.death_less_than_80
    else:
        return variables.death_more_than_80


def get_infection_probability(wears_mask):
    if wears_mask:
        return variables.probability_of_spread_wearing_mask
    else:
        return variables.probability_of_spread_not_wearing_mask


class Person:
    def __init__(self, start_x, start_y, id_number, to_print=False):
        self.id_number = id_number

        # Personal attributes
        self.gender = choice(["male", "female"])
        self.firstname = get_first_name(self.gender)
        self.surname = get_last_name()
        self.age = randint(variables.minimum_age,
                           variables.maximum_age)

        # Habitual attributes
        self.wears_mask = choices(population=[True, False],
                                  cum_weights=[variables.probability_of_wearing_mask,
                                               1 - variables.probability_of_wearing_mask],
                                  k=1)[0]

        self.probability_of_infecting = get_infection_probability(self.wears_mask)  # TODO: Add variable infection rate depending on e.g wears a mask
        self.probability_of_death = get_death_probability(self.age)  # TODO: Add probability of death depending on gender

        # Position of person
        self.x = start_x
        self.y = start_y

        # Initial condition of person
        self.condition = State()

        self.generation_infected = None
        self.generation_immune = None

        self.to_print = to_print

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
        self.generation_infected = generation
        self.condition.becomes_infected()
        print_if(self.to_print, self.firstname + " " + self.surname + " (ID:" + str(
            self.id_number) + ") has been infected in generation " + str(generation) + ".")

    def dies(self, generation):
        self.condition.dies()
        print_if(self.to_print,
                 self.firstname + " " + self.surname + " (ID:" + str(self.id_number) + ") has died, age " + str(
                     self.age) + ", in generation " + str(generation) + ".")
        return self

    def recover(self, generation):
        self.generation_immune = generation
        self.condition.recover()
        print_if(self.to_print,
                 self.firstname + " " + self.surname + " (ID:" + str(self.id_number) + ")" + ", age " + str(
                     self.age) + ", is now immune as of generation " + str(generation) + ".")
        return self

    def immunity_wears(self, generation):
        self.condition.immunity_wears()
        print_if(self.to_print, self.firstname + " " + self.surname + " (ID:" + str(self.id_number) + "), age " + str(
            self.age) + ", is no longer immune as of generation " + str(generation) + ".")
        return self

    # Boolean variables to test the state
    def is_infected(self):
        return self.condition.is_infected

    def is_dead(self):
        return self.condition.is_dead

    def is_healthy(self):
        return self.condition.is_healthy

    def is_immune(self):
        return self.condition.is_immune

    # Methods to infect or have a person die
    def maybe_infect(self, neighbour, generation):
        c = choices(population=["infect", "nothing"],
                    cum_weights=[self.probability_of_infecting, 1 - self.probability_of_infecting],
                    k=1)[0]
        if c == "infect":
            neighbour.infected(generation)  # Fine to infect both if one is already infected
            return neighbour
        else:
            return None

    def maybe_die(self, generation):
        c = choices(population=["dies", "nothing"],
                    cum_weights=[self.probability_of_death, 1 - self.probability_of_death],
                    k=1)[0]
        if c == "dies":
            self.dies(generation)
            return self
        else:
            return None
