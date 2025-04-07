from collections import Counter, OrderedDict
import numpy as np


class huffman:
    def __init__(self, wort):
        word_len = len(wort)
        c_count = Counter(wort)

        prob = sorted(c_count.items(), key=lambda x: x[1], reverse=True)
        prob_map = dict([(p[0], p[1] / word_len) for p in prob])
        prob.reverse()

        tmp_code = OrderedDict.fromkeys(wort, "")

        i = 0
        for _ in iter(int, 1):
            first = prob[i]
            second = prob[i + 1]
            i += 2

            # append the code, we will have to reverse the code
            for char in first[0]:
                tmp_code[char] += "1"
            for char in second[0]:
                tmp_code[char] += "0"
            new_word = first[0] + second[0]
            new_prob = first[1] + second[1]

            # find the index of the next position
            j = 0
            for c, p in prob:
                if p > new_prob:
                    break
                j += 1

            prob.insert(j, (new_word, new_prob))
            if new_prob >= word_len:
                break

        self.code_template = dict([(t[0], t[1][::-1]) for t in tmp_code.items()])
        self.av_char_length = np.sum(
            [(p * len(self.code_template[c])) for (c, p) in prob_map.items()]
        )
        entropy = np.sum([p * np.log2(1 / p) for (_, p) in prob_map.items()])
        self.redundancy = self.av_char_length - entropy

    def encode(self, wort):
        result = ""
        for char in wort:
            if char in self.code_template:
                code = self.code_template[char]
                result += code
            else:
                raise ValueError(f"{char} not in mapping")

        wort_count = Counter(wort)
        wort_len = len(wort)
        wort_prob = dict([(p[0], p[1] / wort_len) for p in wort_count.items()])

        av_char_length = np.sum(
            [wort_prob[c] * len(self.code_template[c]) for c in wort_prob]
        )
        entropy = np.sum([p * np.log2(1 / p) for (_, p) in wort_prob.items()])
        redundancy = av_char_length - entropy
        return result, av_char_length, redundancy

    def decode(self, code):
        wort = ""
        remainder = code

        while remainder:
            for char, code in self.code_template.items():
                if remainder.startswith(code):
                    wort += char
                    remainder = remainder[len(code) :]
                    break

        return wort


h = huffman("HOCHSCHULE")
print(h.code_template)
print("Mittlere Codewortlänge: ", h.av_char_length)
print("Redundanz: ", h.redundancy)
print(h.encode("HHHHH"))
print(h.encode("EEEEE"))
print(h.encode("HOCH"))

code, _, _ = h.encode("HULE")
print(code)
print(h.decode(code))
