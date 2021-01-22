from person import Person, print_if
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns
import variables
import time
from datetime import datetime, timedelta

# Global variables for spacing printing
spaces_per_square = 12
end_spaces = 50


# Static helper methods
def max_difference(array):
    value_minimum = array[0]
    difference_max = 0
    for i in range(len(array)):
        if array[i] < value_minimum:
            value_minimum = array[i]
        elif array[i] - value_minimum > difference_max:
            difference_max = array[i] - value_minimum
    return difference_max


def seven_day_average(array):
    res = []
    while len(array) > 7:
        res.append(sum(array[:7]) / 7)
        array = array[7:]
    return max_difference(res)


def update_lists(add_to, remove_from, person):
    if person is not None:
        add_to.add(person)
        remove_from.remove(person)


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

        self.distance_to_infect = variables.distance_to_infect  # In squares
        self.immunity_lasts_for = variables.immunity_lasts_for  # Generations
        self.infection_lasts_for = variables.infection_lasts_for  # Generations

        # Sets to iterate through
        self.those_healthy = set()
        self.those_infected = set()
        self.those_immune = set()
        self.those_dead = set()

        # If want to print interim results and generations
        self.to_print = to_print

        # Required Data for plotting
        self.healthy_over_time = []
        self.infected_over_time = []
        self.immune_over_time = []
        self.dead_over_time = []

    # Move a person in the environment
    def move(self, person):
        z = variables.maximum_squares_to_move
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

    def current_date(self):
        return self.start_date + timedelta(days=self.generation)

    # Print methods
    def print(self):
        print("Current Generation:", self.generation)
        print("Date:", format_date(self.current_date()))
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
        print("Simulation Set Up for %s" % variables.disease_name)
        print("Beginning simulation on %s" % format_date(self.current_date()))
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
        print("Date:", format_date(self.current_date()), "\n")

        print("%i Healthy People" % len(self.those_healthy))
        print("%i Infected People" % len(self.those_infected))
        print("%i Dead People" % len(self.those_dead))
        print("%i Immune People\n" % len(self.those_immune))

        dead_percent = len(self.those_dead) * 100 / len(self.people)
        print("%.2f%% of people were killed" % dead_percent)

        max_deaths = max_difference(self.dead_over_time)
        print("There was a high of %i deaths in one day" % max_deaths)
        avg_deaths = seven_day_average(self.dead_over_time)
        print("There was a high of %i deaths on average over 7 days\n" % avg_deaths)

        max_infections = max_difference(self.infected_over_time)
        print("There was a high of %i infections in one day" % max_infections)
        avg_infections = seven_day_average(self.infected_over_time)
        print("There was a high of %i deaths on average over 7 days\n" % avg_infections)

        try:
            eradication = self.infected_over_time.index(0)
            print(variables.disease_name, "was eradicated in generation", eradication)
        except ValueError:
            print(variables.disease_name, "was not eradicated")

        print("-" * end_spaces)

    # Generation methods
    def generate_one(self):
        # Move people
        for person in self.people:
            self.move(person)
        self.generation += 1

        # Infect people
        for person in self.those_infected.copy():
            for neighbour in self.healthy_people_in_proximity(person):
                if person.distance_to(neighbour) <= self.distance_to_infect:
                    update_lists(add_to=self.those_infected,
                                 remove_from=self.those_healthy,
                                 person=person.maybe_infect(neighbour, self.generation))

            # Determine if a person dies
            update_lists(add_to=self.those_dead,
                         remove_from=self.those_infected,
                         person=person.maybe_die(self.generation))

            # Check whether a person has recovered and hasn't already died
            if self.generation - self.infection_lasts_for == person.generation_infected and not person.is_dead():
                update_lists(add_to=self.those_immune,
                             remove_from=self.those_infected,
                             person=person.recover(self.generation))

        # Check whether a person has had their immunity worn off
        for person in self.those_immune.copy():
            if self.generation - self.immunity_lasts_for == person.generation_immune:
                update_lists(add_to=self.those_healthy,
                             remove_from=self.those_immune,
                             person=person.immunity_wears(self.generation))

    def generate_n(self, n):
        print("Simulating %i generations\n" % n)
        start_time = time.time()
        for i in range(n):
            self.generate_one()

            self.healthy_over_time.append(self.calculate_statistics("HEALTHY")[1])
            self.immune_over_time.append(self.calculate_statistics("IMMUNE")[1])
            self.infected_over_time.append(self.calculate_statistics("INFECTED")[1])
            self.dead_over_time.append(self.calculate_statistics("DEAD")[1])

            if self.to_print:
                self.print()

        print("\nSimulation Complete")
        print("Execution took: %.5f seconds" % (time.time() - start_time))
        print("-" * end_spaces + "\n")

    def plot(self):
        x_range = range(self.generation)

        palette = sns.color_palette("Set1")
        plt.stackplot(x_range,
                      self.healthy_over_time,
                      self.infected_over_time,
                      self.dead_over_time,
                      self.immune_over_time,
                      labels=["Healthy", "Infected", "Dead", "Immune"],
                      colors=palette,
                      alpha=0.4)
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

        plt.xlabel("Generations")
        plt.ylabel("People")
        plt.title("Spread of epidemic over time")

        plt.tight_layout()
        plt.show()

        # self.print()
        # self.print_status()
