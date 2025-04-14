class BlockCode:
    def __init__(self, p, max_corr_bits):
        self.p = p
        self.max_corr_bits = max_corr_bits
        self.H = []
        for i in range(len(p)):
            self.H.append([0]*len(p) + p[i])
            self.H[i][i] = 1

        for x in self.H:
            print(x)

beliebigeMatrix = [[1,0,1,1],[1,1,1,0],[0,1,1,1]]

blockCode = BlockCode(beliebigeMatrix, 2)