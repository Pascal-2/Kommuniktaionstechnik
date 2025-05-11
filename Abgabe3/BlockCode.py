import numpy as np
from itertools import combinations
import kanalFehler


class BlockCode:
    def __init__(self, P: np.ndarray, max_corr_bits: int):
        self.P = P
        self.k, self.p = P.shape
        self.n = self.k + self.p
        self.max_corr_bits = max_corr_bits

        # Erstelle die Generatormatrix G = [I | P]
        I_k = np.eye(self.k, dtype=int)
        self.G = np.concatenate((I_k, self.P), axis=1)

        # Erstelle die Kontrollmatrix H = [P^T | I]
        I_p = np.eye(self.p, dtype=int)
        self.H = np.concatenate((self.P.T, I_p), axis=1)

        # Erstelle Syndrom-Tabelle
        self.S = self._create_syndrome_table()

    def _create_syndrome_table(self):
        S = {}
        # Für 1-Bit Fehler
        for i in range(self.n):
            e = np.zeros(self.n, dtype=int)
            e[i] = 1
            s = tuple(np.matmul(self.H, e.T) % 2)
            S[s] = e

        # Für 2-Bit Fehler (optional, wenn max_corr_bits >= 2)
        if self.max_corr_bits >= 2:
            for i, j in combinations(range(self.n), 2):
                e = np.zeros(self.n, dtype=int)
                e[i], e[j] = 1, 1
                s = tuple(np.matmul(self.H, e.T) % 2)
                if s not in S:
                    S[s] = e
        return S

    def encode(self, message: np.ndarray):
        if len(message) != self.k:
            raise ValueError("Falsche Länge der Nachricht.")
        return np.matmul(message, self.G) % 2

    def decode(self, codeword: np.ndarray):
        if len(codeword) != self.n:
            raise ValueError("Falsche Länge des Codeworts.")

        syndrome = tuple(np.matmul(self.H, codeword.T) % 2)

        if all(bit == 0 for bit in syndrome):
            return codeword[:self.k], 0  # Kein Fehler

        error_vector = self.S.get(syndrome)
        if error_vector is not None:
            corrected_codeword = (codeword + error_vector) % 2
            num_errors = int(np.sum(error_vector))
            return corrected_codeword[:self.k], num_errors

        return None, 0  # Korrektur nicht möglich


def testBlockCode():
    P_7_4_hamming = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1]
    ])
    bc = BlockCode(P_7_4_hamming, 1)
    msg = np.array([1, 0, 1, 1])
    print("Nutzbits:", msg)
    codeword = bc.encode(msg)
    print("Codewort:", codeword)

    # Simuliere Fehler
    Channel = kanalFehler.FixedErrorChannel(1)

    received = Channel(codeword)
    decoded, errors = bc.decode(received)
    print("Dekodiert:", decoded, "| Fehler korrigiert:", errors)
    print()

    P_custom1 = np.array([
        [1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1]
    ])
    bc2 = BlockCode(P_custom1, 2)
    msg = np.array([1, 0])
    print("Nutzbits:", msg)
    codeword = bc2.encode(msg)
    print("Codewort:", codeword)

    # Simuliere Fehler
    Channel = kanalFehler.FixedErrorChannel(2)

    received = Channel(codeword)
    decoded, errors = bc2.decode(received)
    print("Dekodiert:", decoded, "| Fehler korrigiert:", errors)
    print()

    P_custom2 = np.array([
        [1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 1]
    ])
    bc3 = BlockCode(P_custom2, 2)
    msg = np.array([1, 0, 1])
    print("Nutzbits:", msg)
    codeword = bc3.encode(msg)
    print("Codewort:", codeword)

    # Simuliere Fehler
    Channel = kanalFehler.FixedErrorChannel(2)

    received = Channel(codeword)
    decoded, errors = bc3.decode(received)
    print("Dekodiert:", decoded, "| Fehler korrigiert:", errors)

