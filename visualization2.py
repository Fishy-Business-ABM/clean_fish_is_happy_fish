from execute import execute
import matplotlib.pyplot as plt

out = execute(
    nb_food=10,
    nb_initial_fish=100,
    nb_sharks=1,
    mass_fish=0.0001,
    food_regrowth_rate=0.005,
    max_runtime=100
    )
out_food = out[0]
out_fish = out[1]
out_shark = out[2]

food_coords = []
fish_coords = []
shark_coords = []

for time in range(len(out_fish)):
    for food in out_food[time]:
        plt.plot([food["pos"][0]], [food["pos"][1]], 'bo')

    for fish in out_fish[time]:
        plt.plot([fish["pos"][0]], [fish["pos"][1]], 'ro')

    for shark in out_shark[time]:
        plt.plot([shark["pos"][0]], [shark["pos"][1]], 'go')

    plt.suptitle("Frame %i/%i" %(time+1,len(out_fish)))
    plt.xlim(0,800)
    plt.ylim(0,800)
    plt.draw()
    plt.pause(0.1)
    plt.close()