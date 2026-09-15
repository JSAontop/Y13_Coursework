import random
import time

attempts = 0 

def probs(*events):
    table = []

    for i in events:
        for j in range(i[1]):
            table.append(i[0])

    return random.choice(table)


probs(["blue", 60],
      ["red", 20],
      ["black", 40],
      ["green", 10])

expected = [["blue", 40],
            ["red", 30],
            ["black", 20],
            ["green", 10]]
stats = []
results = []
while expected != stats:
    results = []
    for i in range (100):
        results.append(
            probs(["blue", 40],
                ["red", 30],
                ["black", 20],
                ["green", 10]))

    print("blue",results.count("blue"))
    print("red",results.count("red"))
    print("black",results.count("black"))
    print("green",results.count("green"),"\n")

    stats = [["blue",results.count("blue")],
            ["red",results.count("red")],
            ["black",results.count("black")],
            ["green",results.count("green")]]
    # time.sleep(1)

    attempts = attempts + 1

print(attempts)

stats = [["blue",results.count("blue")],
         ["red",results.count("red")],
         ["black",results.count("black")],
         ["green",results.count("green")]]