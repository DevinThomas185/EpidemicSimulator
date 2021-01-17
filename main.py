from environment import Environment
import matplotlib.pyplot as plt
import seaborn as sns

env = Environment(x=30, y=30)
env.populate(n=500)
#env.print_start()


generations = []
infections = []
deaths = []
healthy = []
immune = []

max_generations = 50
for i in range(max_generations):
    env.generate_one()
    healthy.append(env.calculate_statistics("HEALTHY")[1])
    infections.append(env.calculate_statistics("INFECTED")[1])
    deaths.append(env.calculate_statistics("DEAD")[1])
    immune.append(env.calculate_statistics("IMMUNE")[1])
env.print()

x = range(max_generations)

pal = sns.color_palette("Set1")
plt.stackplot(x, healthy, infections, deaths, immune, labels=["Healthy", "Infected", "Dead", "Immune"], colors=pal, alpha=0.4)
plt.legend(loc='upper right')
plt.show()

env.print_status()

"""
env.generate_n(100)
env.print()
env.print_status()
"""