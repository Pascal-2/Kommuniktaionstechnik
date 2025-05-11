import numpy as np

from Simulator import Simulationsstudie
from BlockCode import BlockCode
from kanalFehler import BSC

P_10_3 = np.array([
        [1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 1],
    ])

bc = BlockCode(P_10_3, 2)
bsc = BSC(0.15)
sim = Simulationsstudie(bc, bsc, len(P_10_3), 1000)
sim.run()


sim_results = sim.results()
sim.plot_results("plot2", sim_results)


