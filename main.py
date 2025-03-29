from math import log2
from matplotlib import pyplot as plt

with open("wortliste.txt", "r", encoding="utf-8") as f:
    words = [l.rstrip() for l in f]



# 1.1
def getInfo(wort_laenge):
    n = len(words)
    woerter_mit_laenge = []
    for x in words:
        if len(x) == wort_laenge:
            woerter_mit_laenge.append(x)
    if not woerter_mit_laenge:
        return 0
    m = len(woerter_mit_laenge)
    return log2(n/m)


laengen = [len(x) for x in words]
max_word_len = max(laengen)

wort_laengen = [i for i in range(1, max_word_len+1)]
laengen_info = [getInfo(x) for x in wort_laengen]

plt.plot(wort_laengen, laengen_info)
plt.xlabel("Wort laenge")
plt.ylabel("Informationsgehalt in Bit")
plt.show()

# 1.2

def getInfo2(pos, character):
    words_7 = [x for x in words if len(x) == 7]
    n = len(words_7)
    filtered = []
    for x in words_7:
        if x.lower()[pos] == character:
            filtered.append(x)
    m = len(filtered)
    return log2(n/m)

testWord = "xylofon"

letters = [x for x in testWord.lower()]
letter_info = [getInfo2(i, x) for i, x in enumerate(letters)]

plt.bar(range(len(letters)), letter_info)
plt.ylabel("Information in Bit")
plt.xlabel("Buchstabe an Position")
plt.xticks(range(len(letters)), letters)
plt.show()

# 1.3

def getInfo3(in_str, direction):

    n = len([x for x in words if len(x) >= len(in_str)])
    if direction == "forward":
        m = len([x for x in words if x.startswith(in_str)])
    else:
        m = len([x for x in words if x.endswith(in_str)])
    if m == 0:
        return 0
    return log2(n/m)

testWord = "xylofon"
letters = [x for x in testWord.lower()]
letter_info = [getInfo3(testWord[0: i + 1], "forward") for i in range(len(letters))]

plt.bar(range(len(letters)), letter_info)
plt.ylabel("Kumulierte Information in Bit")
plt.xlabel("Buchstabenfolge bis")
plt.xticks(range(len(letters)), letters)
plt.show()

print("Wenn wir wissen, dass ein Wort mit \"x\" beginnt", letter_info[0], "[Bit]")

testWord = "xylofon"
letters = [x for x in testWord.lower()]
letters.reverse()
letter_info = [getInfo3(testWord[-1 - i: len(letters)], "backward") for i in range(len(letters))]

plt.bar(range(len(letters)), letter_info)
plt.ylabel("Kumulierte Information in Bit")
plt.xlabel("Buchstabenfolge bis")
plt.xticks(range(len(letters)), letters)
plt.show()


print("Wenn wir wissen, dass ein Wort mit \"n\" endet", letter_info[0], "[Bit]")

# 2.1

class Source:
    def __init__(self, word: str):

        self.letters = dict()

        for letter in word.lower():
            # Auftrittswahrscheinlichkeit
            c = 0
            for x in word.lower():
                if x == letter:
                    c += 1
            auftritt = c / len(word)

            info = log2(1 / auftritt)


            self.letters[letter] = (auftritt, info)

        self.entropie = sum([x[0] * x[1] for x in self.letters.values()])

    def __str__(self):
        return str(self.letters) + ", " + str(self.entropie)


test = Source("Hochschule")

print(test)


with open("rfc2324.txt", "r", encoding="utf-8") as f:
    coffeeText = f.read()

test2 = Source(coffeeText)

print(test2)

zeichen1 = list(sorted(list(test2.letters.keys()), key=lambda x: test2.letters[x][1]))
zeichen2 = list(sorted(list(test2.letters.keys()), key=lambda x: test2.letters[x][0]))

infos = [test2.letters[x][1] for x in zeichen1]

haufigkeit = [test2.letters[x][0] for x in zeichen2]

plt.figure(figsize=(21, 9))
plt.bar(range(len(zeichen1)), infos, width=0.4)
plt.ylabel("Informationsgehalt")
plt.xlabel("Zeichen")
plt.xticks(range(len(zeichen1)), zeichen1)
plt.show()

plt.figure(figsize=(21, 9))
plt.bar(range(len(zeichen2)), haufigkeit, width=0.4)
plt.ylabel("Auftrittshäufigkeit")
plt.xlabel("Zeichen")
plt.xticks(range(len(zeichen2)), zeichen2)
plt.show()



