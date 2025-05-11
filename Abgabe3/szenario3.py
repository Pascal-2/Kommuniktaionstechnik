import numpy as np

from Simulator import Simulationsstudie
from BlockCode import BlockCode
from kanalFehler import BSC
import matplotlib.pyplot as plt

P_7_4 = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1]
    ])

P_11_4 = np.array([
        [1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 1]
    ])

y1 = []
y2 = []
x = []

for i in range(201):
    bc1 = BlockCode(P_7_4, 1)
    bc2 = BlockCode(P_11_4, 2)
    err_wahr = i / 1000
    bsc = BSC(err_wahr)
    sim1 = Simulationsstudie(bc1, bsc, len(P_7_4), 1000)
    sim2 = Simulationsstudie(bc2, bsc, len(P_11_4), 1000)
    sim1.run()
    sim2.run()
    sim1_res = sim1.results()
    sim2_res = sim2.results()

    rest_fehler1 = sim1_res["nicht_korrigiert"][1] + sim1_res["fehlerhaft_korrigiert"][1]
    rest_fehler2 = sim2_res["nicht_korrigiert"][1] + sim2_res["fehlerhaft_korrigiert"][1]
    y1.append(rest_fehler1)
    y2.append(rest_fehler2)
    x.append(err_wahr)


plt.plot(x, y1, label="7-4-Code")
plt.plot(x, y2, label="11-4-Code")
plt.xlabel("Bitfehlerwahrscheinlichkeit")
plt.ylabel("Restfehlerwahrscheinlichkeit")
plt.legend()
plt.savefig("plot3.png")


