from collections import Counter
from math import log2
import random


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

#Aufgabe 4
from arithmetic_compressor import AECompressor
from arithmetic_compressor.models import StaticModel

from main import Source

# create the model
#model = StaticModel({'A': 0.5, 'B': 0.25, 'C': 0.25})
with open("rfc2324.txt", 'r', encoding="utf-8") as f:
    text = f.read().lower()
tempdict = Source(text).letters
coffeedict = dict()
for x in tempdict:
    coffeedict[x] = tempdict[x][0]
model = StaticModel(coffeedict)

# create an arithmetic coder
coder = AECompressor(model)

# 1000 random letters from text
from huffman import huffman
shanFaCodierer = Code(text, shannon_fano)
huffCodierer = huffman(text)

tenTries = [[],[],[]]
for i in range(10):
    randomLetters = []
    for _ in range(1000):
        randomIndex = random.randint(0, len(text) - 1)
        randomLetters.append(text[randomIndex])
    # encode some data
    data = "".join(randomLetters)
    N = len(data)
    compressed = coder.compress(data)
    tenTries[0].append(len(compressed) - 4000) # to highlight changes between bars: subtracting most of all bars
    tenTries[1].append(len(shanFaCodierer.encode(data)[0]) - 4000)
    tenTries[2].append(len(huffCodierer.encode(data)[0]) - 4000)

for x in tenTries:
    print(x)

import matplotlib.pyplot as plt

# Data
groups = ['1', '2', '3', '4', '5','6', '7', '8', '9', '10']
bar1 = tenTries[0]  # Data for first bar in each group
bar2 = tenTries[1]  # Data for second bar in each group
bar3 = tenTries[2]  # Data for third bar in each group

# Number of groups
n_groups = len(groups)

# Width of each bar
bar_width = 0.25


# Positions of the bars (shifted by a certain amount to create groups of 3)
index = list(range(n_groups))
plt.figure(figsize=(21, 9))
# Create the plot
fig, ax = plt.subplots()

# Plot the bars
ax.bar([x - bar_width for x in index], bar1, bar_width, label='Arithmetische Codierung')
ax.bar(index, bar2, bar_width, label='Shannon-Fano Codierung')
ax.bar([x + bar_width for x in index], bar3, bar_width, label='Huffman Codierung')

# Labeling
ax.set_xlabel('Groups')
ax.set_ylabel('Codelänge - 4000')
ax.set_title('Vergleich der Codierungsverfahren')
ax.set_xticks(index)
ax.set_xticklabels(groups)
ax.legend()

# Show plot
plt.show()
