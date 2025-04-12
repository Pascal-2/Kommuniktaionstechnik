def encode_lzw(input_string: str) -> list[int]:
    if not input_string:
        return []

    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}

    p = ""
    lzw_code = []

    for c in input_string:
        pc = p + c
        if pc in dictionary:
            p = pc
        else:
            lzw_code.append(dictionary[p])
            dictionary[pc] = dictionary_size
            dictionary_size += 1
            p = c

    if p:
        lzw_code.append(dictionary[p])

    return lzw_code

def decode_lzw(lzw_code: list[int]) -> str:
    if not lzw_code:
        return ""

    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}

    previous_code = lzw_code[0]
    decoded_chars = [dictionary[previous_code]]
    previous_string = dictionary[previous_code]

    for current_code in lzw_code[1:]:
        current_entry = ""
        if current_code in dictionary:
            current_entry = dictionary[current_code]
        elif current_code == dictionary_size:
            current_entry = previous_string + previous_string[0]
        else:
            raise ValueError(f"Bad compressed code: {current_code}")

        decoded_chars.append(current_entry)

        dictionary[dictionary_size] = previous_string + current_entry[0]
        dictionary_size += 1

        previous_string = current_entry

    return "".join(decoded_chars)

# Example usage
input_text = "LZWLZ78LZ77LZCLZMWLZAP"
encoded_data = encode_lzw(input_text)
decoded_text = decode_lzw(encoded_data)

print(f"Original:   {input_text}")
print(f"Encoded:    {encoded_data}")
print(f"Decoded:    {decoded_text}")
print(f"Original == Decoded: {input_text == decoded_text}")

# Example with KWK case
abababa_enc = encode_lzw("abababa")
abababa_dec = decode_lzw(abababa_enc)
print(f"\nEncoding 'abababa': {abababa_enc}")
print(f"Decoding {abababa_enc}: '{abababa_dec}'")