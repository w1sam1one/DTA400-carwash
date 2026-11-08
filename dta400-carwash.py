import random
import statistics

mean_wash = 5
cars = 200000
runs = 10
loads = [0.5, 0.6, 0.7, 0.8, 0.9]
types = [("constant", 0), ("exponential", 1), ("high_var", 4)]


def wash_time(kind):
    if kind == "constant":
        return mean_wash
    elif kind == "exponential":
        return random.expovariate(1 / mean_wash)
    else:
        return random.gammavariate(0.25, 20)


def simulate(kind, load):
    arrival_rate = load / mean_wash
    time = 0
    free_at = 0
    waits = []

    for i in range(cars):
        time = time + random.expovariate(arrival_rate)
        start = max(time, free_at)
        free_at = start + wash_time(kind)
        if i >= 2000:
            waits.append(start - time)

    return sum(waits) / len(waits)


print("kind load sim ci theory error")

for kind, cv2 in types:
    for load in loads:
        results = []
        for run in range(runs):
            random.seed(run)
            results.append(simulate(kind, load))

        sim = sum(results) / runs
        ci = 2.262 * statistics.stdev(results) / runs ** 0.5
        theory = load * mean_wash * (1 + cv2) / (2 * (1 - load))
        error = (sim - theory) / theory * 100

        print(kind, load, round(sim, 2), round(ci, 2), round(theory, 2), round(error, 1))
