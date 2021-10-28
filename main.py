from environment import Environment

env = Environment(x=30, y=30, to_print=True)
env.populate(n=500)

env.print_start()
env.generate_n(100)
env.plot("all")
env.print_statistics()


# TODO: Implement pandemic control -> Moving to different countries and spreading to that environment
# TODO: Implement immunity and infections for different strains
# TODO: Make spread dependent on strain
# TODO: Remove dead from environment
# TODO: Add in procedures, e.g social distancing, mask promotion, and other events that affect spread
# TODO: Add households / close contact spread
# TODO: Add probability of death depending on gender
# TODO: Add variable infection rate depending on e.g wears a mask
# TODO: Add Testing Procedures
