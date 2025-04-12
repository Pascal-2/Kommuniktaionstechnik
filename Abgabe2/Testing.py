with open("../Abgabe1/rfc2324.txt", "r", encoding="utf-8") as f:
    test = f.read()

from Woerterbuchcodierung import LempelZiv

print(len(test) * 8)

minVal = (-1, -1, 10 ** 1000)
for back_b in range(6, 30):
    for seq_b in range(2, 15):
        lz = LempelZiv(back_b, seq_b)
        current = len(lz.encode(test))
        print(current)
        if current < minVal[2]:
            minVal = (back_b, seq_b, current)
    print(back_b, minVal)
print(minVal)