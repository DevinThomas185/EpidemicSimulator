from person import Person
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns
import variables

spaces = 12  # Global variables for spacing printing


class Environment:
    def __init__(self, x, y, to_print=False):
        self.x_width = x
        self.y_length = y
        self.spaces_available = x * y
        self.positions = [[None for _ in range(x)] for _ in range(y)]
        self.people = []
        self.generation = 0

        self.distance_to_infect = variables.distance_to_infect # In squares
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
        if 0 < end_y < self.y_length and 0 < end_x < self.x_width:
            if self.positions[end_y][end_x] is None and person.condition.state != "DEAD":
                self.positions[end_y][end_x] = person
                self.positions[person.y][person.x] = None
                person.move(end_x, end_y)

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

    def update_lists(self, add_to, remove_from, person):
        if person is not None:
            add_to.add(person)
            remove_from.remove(person)

    # Print methods
    def print(self):
        print("Current Generation:", self.generation)
        for row in self.positions:
            for name in row:
                if name is None:
                    print("-" + " " * (spaces - 1), end="")
                else:
                    print(name, end="")
                    print(" " * (spaces - len(name.firstname)), end="")
            print("\n", end="")
        print("-" * spaces * self.x_width, "\n")

    def print_start(self):
        print("\n" + "-" * 50)
        print("Simulation Set Up")
        print("There are %i people in the simulation. They are:\n" % len(self.people))
        for person in self.people:
            print(str(person.id_number) + ":", person.firstname, person.surname, "(" + person.gender + ")",
                  "Age: " + str(person.age))
        print()
        self.print()
        print("-" * 50 + "\n")

    def print_status(self):
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

        print("-" * 50)

    # Generation methods
    def generate_one(self):
        # Move people
        for person in self.people:
            self.move(person)
        self.generation += 1

        # Infect people
        for person1 in self.people:
            for person2 in self.people[self.people.index(person1) + 1:]:
                if person1.distance_to(person2) <= self.distance_to_infect:
                    if person1.is_infected() and person2.is_healthy():
                        self.update_lists(add_to=self.those_infected,
                                          remove_from=self.those_healthy,
                                          person=person1.maybe_infect(person2, self.generation))
                    elif person1.is_healthy() and person2.is_infected():
                        self.update_lists(add_to=self.those_infected,
                                          remove_from=self.those_healthy,
                                          person=person2.maybe_infect(person1, self.generation))

        # Determine if a person dies
        for person in self.those_infected.copy():
            if person.is_infected:
                self.update_lists(add_to=self.those_dead,
                                  remove_from=self.those_infected,
                                  person=person.maybe_die(self.generation))

        # Check whether a person has recovered
        for person in self.those_infected.copy():
            if person.is_infected:
                if self.generation - self.infection_lasts_for == person.generation_infected and person.is_infected():
                    self.update_lists(add_to=self.those_immune,
                                      remove_from=self.those_infected,
                                      person=person.recover(self.generation))

        # Check whether a person has had their immunity worn off
        for person in self.those_immune.copy():
            if person.is_immune:
                if self.generation - self.immunity_lasts_for == person.generation_immune and person.is_immune():
                    self.update_lists(add_to=self.those_healthy,
                                      remove_from=self.those_immune,
                                      person=person.immunity_wears(self.generation))

    def generate_n(self, n):
        print("Simulating %i generations\n" % n)
        for i in range(n):
            self.generate_one()

            self.healthy_over_time.append(self.calculate_statistics("HEALTHY")[1])
            self.immune_over_time.append(self.calculate_statistics("IMMUNE")[1])
            self.infected_over_time.append(self.calculate_statistics("INFECTED")[1])
            self.dead_over_time.append(self.calculate_statistics("DEAD")[1])

            if self.to_print:
                self.print()

        print("\nSimulation Complete")
        print("-" * 50 + "\n")

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
        plt.legend(loc='upper right')
        plt.show()

        self.print()
        self.print_status()

