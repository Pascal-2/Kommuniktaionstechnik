from collections import Counter
from math import log2

def help1(li, lo, hi):
    c = 0
    for i in range(lo, hi + 1):
        c += li[i][1]

    m = c / 2

    c = 0
    for i in range(lo, hi + 1):
        c += li[i][1]
        if c > m:
            d = abs(m - c)
            od = abs(m - (c - li[i][1]))
            if d <= od:
                return i
            return i - 1

def help2(li, res, lo, hi):
    if hi <= lo:
        return
    teiler = help1(li, lo, hi)

    for i in range(lo, teiler + 1):
        res[li[i][0]] = res[li[i][0]] + "0"
    for i in range(teiler + 1, hi + 1):
        res[li[i][0]] = res[li[i][0]] + "1"

    help2(li, res, lo, teiler)
    help2(li, res, teiler + 1, hi)


def shannon_fano(input_text):


    letters = [x for x in input_text.lower()]
    items_count = sorted(list(Counter(letters).items()), key=lambda x: x[1], reverse=True)

    result = dict()
    for x, _ in items_count:
        result[x] = ""

    help2(items_count, result, 0, len(items_count) - 1)

    return result


print(shannon_fano("kommunikationstechnik"))

def redundacy():
    pass

class Code:
    def __init__(self, nachrichtenquelle, codierungsvorschrift):
        self.nachrichtenquelle = nachrichtenquelle.lower()
        self.codierungsvorschrift = codierungsvorschrift

        self.codierung = codierungsvorschrift(nachrichtenquelle)
        self.decodierung = dict()
        for x in self.codierung:
            self.decodierung[self.codierung[x]] = x
        self.mittlere_codewortlaenge = 0
        for x in self.codierung:
            self.mittlere_codewortlaenge += len(self.codierung[x])
        self.mittlere_codewortlaenge /= len(self.codierung)

        self.letters = dict()
        mittlerer_informationsgehalt = 0
        for letter in nachrichtenquelle.lower():
            # Auftrittswahrscheinlichkeit
            c = 0
            for x in nachrichtenquelle.lower():
                if x == letter:
                    c += 1
            auftritt = c / len(nachrichtenquelle)

            info = log2(1 / auftritt)
            mittlerer_informationsgehalt += info
        mittlerer_informationsgehalt /= len(nachrichtenquelle)

        self.redundanz = self.mittlere_codewortlaenge - mittlerer_informationsgehalt

    def encode(self, word):
        word = word.lower()
        codes = [self.codierung[x] for x in word]
        code = "".join(codes)
        av_char_length = sum([len(x) for x in codes]) / len(codes)
        avg_info = 0
        for letter in word.lower():
            c = 0
            for x in word.lower():
                if x == letter:
                    c += 1
            auftritt = c / len(word)

            info = log2(1 / auftritt)
            avg_info += info
        avg_info /= len(word)
        redundancy = av_char_length - avg_info
        return code, av_char_length, redundancy





    def decode(self, word):
        # word=decode(code)
        res = ""
        cur = ""
        ind = 0
        while True:
            if ind == len(word):
                break
            cur += word[ind]
            ind += 1
            if cur in self.decodierung:
                res += self.decodierung[cur]
                cur = ""
        return res

# Klasse Code testen

a = Code("Hochschule", shannon_fano)
b = a.encode("HHHHHsucseeollll")
print(b)
print(a.decode(b[0]))

c = a.encode("EEEEE")
print(c)
print(a.decode(c[0]))
