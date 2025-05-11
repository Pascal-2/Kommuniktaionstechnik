import numpy as np
import random


# Hilfsfunktion zum Umdrehen von Bits
def flip_bits(bit_vector, positions):
    """Dreht Bits an den angegebenen Positionen im Bitvektor um."""
    flipped_vector = np.copy(bit_vector)
    for pos in positions:
        if 0 <= pos < len(flipped_vector):
            flipped_vector[pos] = 1 - flipped_vector[pos]
    return flipped_vector


# --- 3. Bitfehler / Kanalmodell ---

class BSC:
    """Binär-Symmetrischer Kanal."""

    def __init__(self, p_error):
        if not (0 <= p_error <= 1):
            raise ValueError("Fehlerwahrscheinlichkeit p muss zwischen 0 und 1 liegen.")
        self.p_error = p_error

    def __call__(self, bit_vector):
        """Überträgt den Bitvektor und fügt Fehler gemäß p_error ein."""
        if not isinstance(bit_vector, np.ndarray):
            bit_vector = np.array(bit_vector)

        received_vector = np.copy(bit_vector)
        for i in range(len(received_vector)):
            if random.random() < self.p_error:
                received_vector[i] = 1 - received_vector[i]
        return received_vector


class FixedErrorChannel:
    """Kanal mit fester Anzahl an Bitfehlern pro Codewort."""

    def __init__(self, num_errors):
        if num_errors < 0:
            raise ValueError("Anzahl der Fehler muss nicht-negativ sein.")
        self.num_errors = num_errors

    def __call__(self, bit_vector):
        """Überträgt den Bitvektor und fügt eine feste Anzahl Fehler ein."""
        if not isinstance(bit_vector, np.ndarray):
            bit_vector = np.array(bit_vector)

        n = len(bit_vector)
        if self.num_errors > n:
            # Mehr Fehler als Bits -> alle Bits flippen (oder Fehler werfen)
            # Hier: Flippen aller Bits, wenn num_errors > n
            # Alternativ könnte man auch nur n Bits flippen oder einen Fehler werfen.
            # Für den Test der Korrekturfähigkeit ist es wichtig, dass exakt num_errors
            # Fehler gesetzt werden, wenn num_errors <= n.
            print(f"Warnung: num_errors ({self.num_errors}) > Nachrichtenlänge ({n}). Es werden alle Bits geflippt.")
            error_positions = list(range(n))
        elif self.num_errors == 0:
            return np.copy(bit_vector)
        else:
            # Wähle num_errors zufällige, eindeutige Positionen
            error_positions = random.sample(range(n), self.num_errors)

        return flip_bits(bit_vector, error_positions)