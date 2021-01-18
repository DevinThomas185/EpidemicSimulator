from environment import Environment

env = Environment(x=30, y=30, to_print=False)
env.populate(n=500)

env.print_start()
env.generate_n(300)
env.plot()


# TODO: Implement pandemic control -> Moving to different countries and spreading to that environment
# TODO: Implement immunity and infections for different strains
# TODO: Make spread dependent on strain
# TODO: Remove dead from environment
# TODO: Add in procedures, e.g social distancing, mask promotion, and other events that affect spread
