from variables import *
from random import choices


def procedure(people, sample_size, env):
    if len(people) > 0:
        being_tested = choices(population=people,
                               k=sample_size)
        for person in being_tested:
            test(person, env)


def test(person, env):
    infected = False
    if person.is_infected():
        infected = choices(population=[False, True],
                           cum_weights=[probability_of_false_negative, 1 - probability_of_false_negative],
                           k=1)[0]
    elif person.is_healthy():
        infected = choices(population=[True, False],
                           cum_weights=[probability_of_false_positive, 1 - probability_of_false_positive],
                           k=1)[0]

    # What to do when infected
    if infected and not person.is_isolating:
        print(person, "has begun isolating FOREVER")
        env.those_isolating.add(person)
        person.begin_isolating()
        env.remove_from_positions(person)
