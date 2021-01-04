import matplotlib.pyplot as plt
import numpy as np
import os

arquivo = os.path.join(os.path.dirname(__file__), "saves/plot.csv")
data = np.genfromtxt(
    arquivo, delimiter=",", skip_header=10, skip_footer=10, names=["x", "y"]
)

plt.plot(data["x"], data["y"], color="r", label="Learning")
plt.xlabel("GENERATION")
plt.ylabel("FITNESS")
plt.show()