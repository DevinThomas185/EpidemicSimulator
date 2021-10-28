import matplotlib.pyplot as plt
import seaborn as sns

palette = sns.color_palette("Set1")
colours = ["palegreen", "gold", "darkred", "dodgerblue"]


def stacked(env):
    x_range = range(env.generation)

    plt.stackplot(x_range,
                  env.healthy_over_time,
                  env.infected_over_time,
                  env.dead_over_time,
                  env.immune_over_time,
                  labels=["Healthy", "Infected", "Dead", "Immune"],
                  colors=colours,
                  alpha=0.4)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    plt.xlabel("Generations")
    plt.ylabel("People")
    plt.title("Spread of epidemic over time")

    plt.tight_layout()
    plt.show()


def line(env):
    x_range = range(env.generation)

    plt.plot(x_range, env.healthy_over_time, 'darkred', label="Healthy")
    plt.plot(x_range, env.infected_over_time, 'palegreen', label="Infected")
    plt.plot(x_range, env.dead_over_time, 'dodgerblue', label="Dead")
    plt.plot(x_range, env.immune_over_time, 'gold', label="Immune")

    plt.xlabel("Generations")
    plt.ylabel("People")
    plt.title("Spread of epidemic over time")

    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

    plt.tight_layout()
    plt.show()


def pie(env):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Healthy', 'Infected', 'Dead', 'Immune'

    sizes = [len(env.those_healthy) * 100/len(env.people),
             len(env.those_infected) * 100/len(env.people),
             len(env.those_dead) * 100/len(env.people),
             len(env.those_immune) * 100/len(env.people)]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,
            colors=colours,
            labels=labels,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title("Spread of states at end of simulation")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

    plt.show()
