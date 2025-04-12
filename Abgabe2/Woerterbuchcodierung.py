
class LempelZiv:
    def __init__(self, back_bits, subsequence_bits):
        self.backBits = back_bits
        self.subsequenceBits = subsequence_bits
        self.backtrackingLimit = 2 ** back_bits - 1
        self.sequenceLimit = 2 ** subsequence_bits - 1

    def encode(self, message):
        res = []
        i = 0
        while i < len(message):
            sub = message[max(0, i - self.backtrackingLimit): i]

            indices = []
            for j, y in enumerate(sub):
                if message[i] == y:
                    indices.append(j)

            indices_and_len = []
            for ind in indices:
                c = 0
                while i + c < len(message) and message[i + c] == message[ind + c]:
                    c += 1
                if c < self.subsequenceBits:
                    indices_and_len.append((ind, c))

            indices_and_len = sorted(indices_and_len, key=lambda x: (x[1], x[0]))

            if indices_and_len:
                copy_index, n = indices_and_len[-1]
            else:
                copy_index, n = 0, 0


            if i + n == len(message):
                next = message[i + n - 1]
                n -= 1
            else:
                next = message[i + n]
            res.append((0 if n == 0 else i - copy_index, n, next))
            i += n + 1
        # print(res)
        return "".join([format(x[0], f"0{self.backBits}b") + format(x[1], f"0{self.subsequenceBits}b") + format(ord(x[2]), "08b") for x in res])




    def decode(self, bitstring):
        tup_len = (self.backBits + self.subsequenceBits + 8)
        num_of_tup = int(len(bitstring)/tup_len)
        tuples = []
        for i in range(0, num_of_tup * tup_len, tup_len):
            cur_tup = bitstring[i : i + tup_len]
            back = int(cur_tup[: self.backBits], 2)
            subseq = int(cur_tup[self.backBits : self.backBits + self.subsequenceBits], 2)
            end_char = chr(int(cur_tup[self.backBits + self.subsequenceBits :], 2))
            tuples.append((back, subseq, end_char))
        # print(tuples)

        message = []
        for i in range(num_of_tup):
            sequence = []
            for j in range(len(message) - tuples[i][0], len(message) - tuples[i][0] + tuples[i][1]):
                sequence.append(message[j])
            sequence.append(tuples[i][2])
            message += sequence
        return "".join(message)

# Tests
a = LempelZiv(6, 5)

testBanane = "BANANENANBAU"
res_testBanane = a.encode(testBanane)
print(res_testBanane)
print(a.decode(res_testBanane))

testFisch = "FISCHERSFRITZFISCHTFRISCHEFISCHE"
res_testFisch = a.encode(testFisch)
print(res_testFisch)
print(a.decode(res_testFisch))

