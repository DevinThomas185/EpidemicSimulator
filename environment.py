from datetime import datetime, timedelta
from person import Person, print_if
from random import randint
import numpy as np
import plot
import testing
import time
from variables import *

# Global variables for spacing printing
spaces_per_square = 12
end_spaces = 50


# Static helper methods
def max_difference(array):
    difference_max = 0
    for i in range(len(array) - 1):
        diff = array[i + 1] - array[i]
        if diff > difference_max:
            difference_max = diff
    return difference_max


def seven_day_average(array):
    res = []
    while len(array) > 7:
        res.append(sum(array[:7]) / 7)
        array = array[7:]
    return max_difference(res)


def format_date(date):
    return date.strftime("%d %B %Y")


class Environment:
    def __init__(self, x, y, to_print=False, start_date=datetime.today()):
        self.x_width = x
        self.y_length = y
        self.spaces_available = x * y
        self.positions = [[None for _ in range(x)] for _ in range(y)]
        self.people = []

        self.start_date = start_date
        self.generation = 0

        self.distance_to_infect = distance_to_infect  # In squares
        self.immunity_lasts_for = immunity_lasts_for  # Generations
        self.infection_lasts_for = infection_lasts_for  # Generations

        # Sets to iterate through
        self.those_healthy = set()
        self.those_infected = set()
        self.those_immune = set()
        self.those_dead = set()
        self.those_isolating = set()

        # If want to print interim results and generations
        self.to_print = to_print

        # Required Data for plotting
        self.healthy_over_time = []
        self.infected_over_time = []
        self.immune_over_time = []
        self.dead_over_time = []

    # Move a person in the environment
    def move(self, person):
        z = maximum_squares_to_move
        end_x = person.x + randint(-z, z)
        end_y = person.y + randint(-z, z)
        if 0 <= end_y < self.y_length and 0 <= end_x < self.x_width:
            if self.positions[end_y][end_x] is None and person.condition.state != "DEAD":
                self.positions[end_y][end_x] = person
                self.positions[person.y][person.x] = None
                person.move(end_x, end_y)

    def healthy_people_in_proximity(self, person):
        healthy_people = []
        for i in range(person.x - self.distance_to_infect, person.x + self.distance_to_infect + 1):
            for j in range(person.y - self.distance_to_infect, person.y + self.distance_to_infect + 1):
                if 0 <= i < self.x_width and 0 <= j < self.y_length:
                    p = self.positions[j][i]
                    if p is not None and p.is_healthy():
                        if not person.is_isolating and not p.is_isolating:
                            if self.positions[person.y][person.x].distance_to(p) <= self.distance_to_infect:
                                healthy_people.append(p)
        return healthy_people

    # Populate the environment with people
    def populate(self, n):
        added = 0
        if n > self.spaces_available:
            return "Error"
        while 0 < n <= self.spaces_available:
            x = randint(0, self.x_width - 1)
            y = randint(0, self.y_length - 1)
            if self.positions[y][x] is None:
                person = Person(start_x=x, start_y=y, id_number=added, to_print=self.to_print)
                self.people.append(person)
                self.positions[y][x] = person
                n -= 1
                added += 1
        self.people[0].condition.becomes_infected()  # infect first victim
        self.those_infected.add(self.people[0])
        self.those_healthy.update([x for x in self.people if x.is_healthy()])

    # Helper methods
    def calculate_statistics(self, stat):
        x = [person for person in self.people if person.condition.state == stat]
        return x, len(x)

    def get_current_date(self):
        return (self.start_date + timedelta(days=self.generation)).strftime("%d %B %Y")

    def update_lists(self, add_to, remove_from, person):
        if person is not None:
            add_to.add(person)
            remove_from.remove(person)
            if add_to == self.those_dead:
                self.remove_from_positions(person)

    def remove_from_positions(self, person):
        self.positions[person.y][person.x] = None

    # Print methods
    def print(self):
        print("Current Generation:", self.generation)
        print("Date:", self.get_current_date())
        for row in self.positions:
            for name in row:
                if name is None:
                    print("-" + " " * (spaces_per_square - 1), end="")
                else:
                    print(name, end="")
                    print(" " * (spaces_per_square - len(name.firstname)), end="")
            print("\n", end="")
        print("-" * spaces_per_square * self.x_width, "\n")

    def print_start(self):
        print("\n" + "-" * end_spaces)
        print("Simulation Set Up for %s" % disease_name)
        print("Beginning simulation on %s" % self.get_current_date())
        print("There are %i people in the simulation." % len(self.people), end=" ")
        if self.to_print:
            print_if(self.to_print, "They are:\n")
            for person in self.people:
                print(str(person.id_number) + ":", person.firstname, person.surname, "(" + person.gender + ")",
                      "Age: " + str(person.age))
        print()
        if self.to_print:
            self.print()
        print("-" * end_spaces + "\n")

    def print_status(self):
        print("-" * end_spaces)

        print("Current Status of People\n")
        print("Started with %i people in the simulation" % len(self.people))
        print("%i healthy" % len(self.those_healthy), end=": ")
        print(list(self.those_healthy))
        print("%i infected" % len(self.those_infected), end=": ")
        print(list(self.those_infected))
        print("%i immune" % len(self.those_immune), end=": ")
        print(list(self.those_immune))
        print("%i dead" % len(self.those_dead), end=": ")
        print(list(self.those_dead))

        print("-" * end_spaces)

    def print_statistics(self):
        print("-" * end_spaces)
        print("Generation Statistics at Generation %i" % self.generation)
        print("Date:", self.get_current_date(), "\n")

        print("%i Healthy" % len(self.those_healthy))
        print("%i Infected" % len(self.those_infected))
        print("%i Dead" % len(self.those_dead))
        print("%i Immune\n" % len(self.those_immune))

        dead_percent = len(self.those_dead) * 100 / len(self.people)
        print("%.2f%% of people were killed" % dead_percent)

        max_deaths = max_difference(self.dead_over_time)
        print("There was a high of %i deaths in one day" % max_deaths)
        x = list(self.dead_over_time)
        avg_deaths = seven_day_average([t - s for s, t in zip(x, x[1:])])
        print("There was a high of %i deaths on average over 7 days\n" % avg_deaths)

        max_infections = max_difference(self.infected_over_time)
        print("There was a high of %i infections in one day" % max_infections)
        x = list(self.infected_over_time)
        avg_infections = seven_day_average([t - s for s, t in zip(x, x[1:])])
        print("There was a high of %i infections on average over 7 days\n" % avg_infections)

        if len(self.those_dead) > 0:
            avg_age_of_dead = sum([s.age for s in self.those_dead]) / len(self.those_dead)
            print("The average age of those who died was %i" % avg_age_of_dead)
            youngest_death = min([s.age for s in self.those_dead])
            print("The youngest death was %i" % youngest_death)
            oldest_death = max([s.age for s in self.those_dead])
            print("The oldest death was %i\n" % oldest_death)
        if len(self.those_healthy) > 0:
            avg_age_of_healthy = sum([s.age for s in self.those_healthy]) / len(self.those_healthy)
            print("The average age of those who were still healthy was %i\n" % avg_age_of_healthy)

        try:
            eradication = self.infected_over_time.index(0)
            print(disease_name + " was eradicated in generation " + str(eradication)
                  + " on " + format_date(self.start_date + timedelta(eradication)))
        except ValueError:
            print(disease_name, "was not eradicated")

        print("-" * end_spaces)

    # Generation methods
    def generate_one(self):
        # Move people
        for person in self.people:
            self.move(person)
        self.generation += 1

        # Infect people
        print(self.those_isolating)
        for person in self.those_infected.copy() - self.those_isolating:
            for neighbour in self.healthy_people_in_proximity(person):
                if person.distance_to(neighbour) <= self.distance_to_infect:
                    self.update_lists(add_to=self.those_infected,
                                      remove_from=self.those_healthy,
                                      person=person.maybe_infect(neighbour, self.generation))

            # Determine if a person dies
            self.update_lists(add_to=self.those_dead,
                              remove_from=self.those_infected,
                              person=person.maybe_die(self.generation))

            # Check whether a person has recovered and hasn't already died
            if self.generation - self.infection_lasts_for == person.generation_infected and not person.is_dead():
                self.update_lists(add_to=self.those_immune,
                                  remove_from=self.those_infected,
                                  person=person.recover(self.generation))

        # Check whether a person has had their immunity worn off
        for person in self.those_immune.copy():
            if self.generation - self.immunity_lasts_for == person.generation_immune:
                self.update_lists(add_to=self.those_healthy,
                                  remove_from=self.those_immune,
                                  person=person.immunity_wears(self.generation))

        # testing.procedure(self.people, 500, self)  # Test 10 people

        # Add data for statistics
        self.healthy_over_time.append(self.calculate_statistics("HEALTHY")[1])
        self.immune_over_time.append(self.calculate_statistics("IMMUNE")[1])
        self.infected_over_time.append(self.calculate_statistics("INFECTED")[1])
        self.dead_over_time.append(self.calculate_statistics("DEAD")[1])

    def generate_n(self, n):
        print("Simulating %i generations starting on %s\n" % (n, self.get_current_date()))
        start_time = time.time()

        for i in range(n):
            self.generate_one()
            if self.to_print:
                self.print()

        print("Simulation ended on generation %i on %s" % (self.generation, self.get_current_date()))
        print("Execution took %.5f seconds" % (time.time() - start_time))
        print("-" * end_spaces + "\n")

    def plot(self, plot_type):
        if plot_type == "stacked":
            plot.stacked(self)
        if plot_type == "line":
            plot.line(self)
        if plot_type == "pie":
            plot.pie(self)
        if plot_type == "all":
            plot.stacked(self)
            plot.line(self)
            plot.pie(self)
