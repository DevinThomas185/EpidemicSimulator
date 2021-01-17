from environment import Environment

env = Environment(x=10, y=10)
env.populate(n=10)
#env.print_start()

"""
for i in range(100):
    input()
    env.generate_one()
    #env.print()
env.print()
"""

env.generate_n(100)
env.print()
env.print_status()