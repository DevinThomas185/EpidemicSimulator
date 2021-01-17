from person import Person
from random import randint

spaces = 12  # Global variables for spacing printing


class Environment:
    def __init__(self, x, y):
        self.x_width = x
        self.y_length = y
        self.spaces_available = x * y
        self.positions = [[None for _ in range(x)] for _ in range(y)]
        self.people = []
        self.generation = 0
        self.distance_to_infect = 1

    # Move a person in the environment
    def move(self, person):
        end_x = person.x + randint(-1, 1)
        end_y = person.y + randint(-1, 1)
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
                person = Person(start_x=x, start_y=y, id_number=added)
                self.people.append(person)
                self.positions[y][x] = person
                n -= 1
                added += 1
        self.people[0].condition.becomes_infected()  # infect first victim

    # Helper methods
    def calculate_statistics(self, stat):
        x = [person for person in self.people if person.condition.state == stat]
        return x, len(x)

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
        print("There are %i people in the simulation. They are:\n" % len(self.people))
        for person in self.people:
            print(str(person.id_number) + ":", person.firstname, person.surname, "(" + person.gender + ")",
                  "Age: " + str(person.age))
        print()
        self.print()
        print("-" * 50 + "\n")

    def print_status(self):
        (infected, infectedLen) = self.calculate_statistics("INFECTED")
        (healthy, healthyLen) = self.calculate_statistics("HEALTHY")
        (dead, deadLen) = self.calculate_statistics("DEAD")
        (immune, immuneLen) = self.calculate_statistics("IMMUNE")

        print("Current Status of People\n")
        print("Started with %i people in the simulation" % len(self.people))
        print("%i healthy" % healthyLen, end=": ")
        print(healthy)
        print("%i infected" % infectedLen, end=": ")
        print(infected)
        print("%i immune" % immuneLen, end=": ")
        print(immune)
        print("%i dead" % deadLen, end=": ")
        print(dead)

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
                if person1.distance_to(person2) <= self.distance_to_infect \
                        and (person1.is_infected() or person2.is_infected())\
                        and (person1.is_healthy() or person2.is_healthy()):
                    person1.maybe_infect(person2, self.generation)

        # Kill people
        for person in self.people:
            if person.condition.state == "INFECTED":
                person.maybe_die(self.generation)

        # Recover people
        for person in self.people:
            if self.generation - 14 == person.generation_infected and person.is_infected():
                person.recover(self.generation)

    def generate_n(self, n):
        print("Simulating %i generations\n" % n)
        for i in range(n):
            self.generate_one()
        print("\nSimulation Complete")
        print("-" * 50 + "\n")
