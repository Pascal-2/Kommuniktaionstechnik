from BlockCode import BlockCode
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

class Encoder:
    def __init__(self, block_code: BlockCode):
        self.block_code = block_code

    def __call__(self, message):
        return self.block_code.encode(message)


class Decoder:
    def __init__(self, block_code: BlockCode):
        self.block_code = block_code

    def __call__(self, received):
        return self.block_code.decode(received)


def simulate_transmission(block_code: BlockCode, channel, k: int):
    encoder = Encoder(block_code)
    decoder = Decoder(block_code)

    # 1. Quelle: Zufällige Nachricht
    message = np.random.randint(0, 2, k)

    # 2. Codieren
    codeword = encoder(message)

    # 3. Kanal
    received = channel(codeword)

    # 4. Dekodieren
    decoded, corrected_errors = decoder(received)

    # 5. Auswertung
    pre_errors = np.sum(codeword != received)
    if decoded is not None:
        post_errors = np.sum(message != decoded)
        corrected = True
    else:
        post_errors = None
        corrected = False

    return {
        "original_message": message,
        "codeword": codeword,
        "received": received,
        "decoded": decoded,
        "bit_errors_pre": pre_errors,
        "corrected_errors": corrected_errors,
        "bit_errors_post": post_errors,
        "corrected": corrected
    }



class Simulationsstudie:
    def __init__(self, block_code, channel, k, N):
        self.block_code = block_code
        self.channel = channel
        self.k = k
        self.N = N

        # Zählvariablen
        self.total = 0
        self.fehlfrei = 0
        self.korrigiert = 0
        self.nicht_korrigiert = 0
        self.erfolgreich_korrigiert = 0
        self.fehlerhaft_korrigiert = 0

        # Verteilungen
        self.pre_error_dist = Counter()
        self.corrected_error_dist = Counter()
        self.post_error_dist = Counter()

    def run(self):
        for _ in range(self.N):
            result = simulate_transmission(self.block_code, self.channel, self.k)
            self.total += 1

            bit_errors_pre = result["bit_errors_pre"]
            corrected_errors = result["corrected_errors"]
            bit_errors_post = result["bit_errors_post"]
            decoded = result["decoded"]

            # Verteilungen
            self.pre_error_dist[bit_errors_pre] += 1
            if corrected_errors is not None:
                self.corrected_error_dist[corrected_errors] += 1
            if bit_errors_post is not None:
                self.post_error_dist[bit_errors_post] += 1

            if bit_errors_pre == 0:
                self.fehlfrei += 1
            elif decoded is None:
                self.nicht_korrigiert += 1
            else:
                self.korrigiert += 1
                if bit_errors_post == 0:
                    self.erfolgreich_korrigiert += 1
                else:
                    self.fehlerhaft_korrigiert += 1

    def results(self):
        return {
            "gesamt": self.total,
            "fehlfrei": (self.fehlfrei, self.fehlfrei / self.total),
            "korrigiert": (self.korrigiert, self.korrigiert / self.total),
            "nicht_korrigiert": (self.nicht_korrigiert, self.nicht_korrigiert / self.total),
            "erfolgreich_korrigiert": (self.erfolgreich_korrigiert, self.erfolgreich_korrigiert / self.total),
            "fehlerhaft_korrigiert": (self.fehlerhaft_korrigiert, self.fehlerhaft_korrigiert / self.total),
            "verteilung_bitfehler_vor": dict(self.pre_error_dist),
            "verteilung_korrigierter_bits": dict(self.corrected_error_dist),
            "verteilung_bitfehler_nach": dict(self.post_error_dist)
        }

    def plot_results(self, name, sim_results):

        # Bar-Plot 1
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        # Plot 1: Fehlertypen allgemein
        categories_1 = ['Fehlerfrei', 'Korrigiert', 'Nicht korrigiert']
        values_1 = [
            sim_results["fehlfrei"][1],
            sim_results["korrigiert"][1],
            sim_results["nicht_korrigiert"][1]
        ]
        axs[0].bar(categories_1, values_1, color=['green', 'orange', 'red'])
        axs[0].set_title("Szenario 1 – Anteile der Nachrichtenzustände")
        axs[0].set_ylabel("Anteil")
        axs[0].set_ylim(0, 1)

        # Plot 2: Erfolgsbilanz der Korrektur
        categories_2 = ['Fehlerfrei', 'Erfolgreich korrigiert', 'Fehlerhaft korrigiert']
        values_2 = [
            sim_results["fehlfrei"][1],
            sim_results["erfolgreich_korrigiert"][1],
            sim_results["fehlerhaft_korrigiert"][1]
        ]
        axs[1].bar(categories_2, values_2, color=['green', 'blue', 'red'])
        axs[1].set_title("Szenario 1 – Qualität der Korrektur")
        axs[1].set_ylabel("Anteil")
        axs[1].set_ylim(0, 1)

        # Plot 3: Verteilungen (Fehleranzahl)
        width = 0.3
        pre = sim_results["verteilung_bitfehler_vor"]
        cor = sim_results["verteilung_korrigierter_bits"]
        post = sim_results["verteilung_bitfehler_nach"]

        keys = sorted(set(pre.keys()).union(cor.keys()).union(post.keys()))
        x = np.arange(len(keys))

        pre_vals = [pre.get(k, 0) for k in keys]
        cor_vals = [cor.get(k, 0) for k in keys]
        post_vals = [post.get(k, 0) for k in keys]

        axs[2].bar(x - width, pre_vals, width, label='Vor Korrektur', color='gray')
        axs[2].bar(x, cor_vals, width, label='Korrigiert', color='orange')
        axs[2].bar(x + width, post_vals, width, label='Nach Korrektur', color='green')
        axs[2].set_xticks(x)
        axs[2].set_xticklabels(keys)
        axs[2].set_title("Szenario 1 – Verteilungen der Bitfehler")
        axs[2].set_ylabel("Anzahl")
        axs[2].legend()

        plt.tight_layout()
        plt.savefig(f"{name}.png")
