from collections import Counter

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