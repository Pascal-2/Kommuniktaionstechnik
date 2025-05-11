import numpy as np

from Simulator import Simulationsstudie
from BlockCode import BlockCode
from kanalFehler import BSC

P_7_4_hamming = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1]
    ])

bc = BlockCode(P_7_4_hamming, 1)
bsc = BSC(0.05)
sim = Simulationsstudie(bc, bsc, len(P_7_4_hamming), 1000)
sim.run()


sim_results = sim.results()
sim.plot_results("plot1", sim_results)


