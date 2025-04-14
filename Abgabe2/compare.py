from Woerterbuchcodierung import LempelZiv
import Lempel_Ziv_Welch

with open("rfc2324.txt", "r", encoding="utf-8") as f:
    test = f.read()

a = LempelZiv(15, 9)

res_len_lz = len(a.encode(test))
res_len_lzw = len(Lempel_Ziv_Welch.encode_lzw_to_bits(test))

print(res_len_lz, res_len_lzw, len(test)*8)

print(f"LZW is {round(((res_len_lz / res_len_lzw) - 1) * 100, 2)}% better than LZ")