def encode_lzw_to_bits(input_string: str) -> str:
    if not input_string:
        return ""

    max_dict_size = 4096
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}

    p = ""
    output_bits = []
    current_bit_width = 9 # Start with 9 bits

    for c in input_string:
        pc = p + c
        if pc in dictionary:
            p = pc
        else:
            code = dictionary[p]
            # Format the code with the current bit width
            output_bits.append(format(code, f'0{current_bit_width}b'))

            # Add new entry if dictionary is not full
            if dictionary_size < max_dict_size:
                dictionary[pc] = dictionary_size
                dictionary_size += 1

                # Check if we need to increase bit width for the *next* code
                # Use >= because dictionary_size represents the *next available* code
                if dictionary_size >= (1 << current_bit_width) and current_bit_width < 12:
                     current_bit_width += 1
            p = c

    # Output the code for the last remaining sequence p
    if p:
         code = dictionary[p]
         output_bits.append(format(code, f'0{current_bit_width}b'))

    return "".join(output_bits)

def decode_lzw_from_bits(input_bitstring: str) -> str:
    if not input_bitstring:
        return ""

    max_dict_size = 4096
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}

    # Read the first code (always assumes initial bit width)
    current_bit_width = 9
    pos = 0
    first_code_bits = input_bitstring[pos:pos + current_bit_width]
    pos += current_bit_width
    previous_code = int(first_code_bits, 2)

    if previous_code not in dictionary:
         raise ValueError(f"Invalid start code: {previous_code}")

    decoded_chars = [dictionary[previous_code]]
    previous_string = dictionary[previous_code]

    while pos < len(input_bitstring):
        # Read the next code using the *current* bit width
        # Check if enough bits remain
        if pos + current_bit_width > len(input_bitstring):
            # Handle potentially incomplete trailing bits if necessary,
            # or raise an error. For simplicity, we'll assume valid input for now.
            # print(f"Warning: Trailing bits detected ({len(input_bitstring) - pos} < {current_bit_width})")
            break # Stop if not enough bits for a full code remain

        code_bits = input_bitstring[pos:pos + current_bit_width]
        current_code = int(code_bits, 2)
        pos += current_bit_width

        current_entry = ""
        if current_code in dictionary:
            current_entry = dictionary[current_code]
        elif current_code == dictionary_size: # KWK case
            current_entry = previous_string + previous_string[0]
        else:
            # Check if code might be valid with a *different* bit width (e.g. due to padding)
            # This simple version assumes perfect sync, so this is an error.
             raise ValueError(f"Bad compressed code: {current_code} at pos {pos - current_bit_width}, dict_size {dictionary_size}, bit_width {current_bit_width}")


        decoded_chars.append(current_entry)

        # Add new entry to dictionary if not full
        if dictionary_size < max_dict_size:
            new_entry = previous_string + current_entry[0]
            dictionary[dictionary_size] = new_entry
            dictionary_size += 1

            # Check if we need to increase bit width for the *next* read
            if dictionary_size >= (1 << current_bit_width) and current_bit_width < 12:
                 current_bit_width += 1

        previous_string = current_entry # Update for next iteration


    return "".join(decoded_chars)



# Example usage
input_text = "LZWLZ78LZ77LZCLZMWLZAP" * 5 # Make it longer to test bit width increase
print(f"Original Length: {len(input_text)}")

encoded_bit_string = encode_lzw_to_bits(input_text)
print(f"Encoded Bit String Length: {len(encoded_bit_string)}")
# Uncomment to see the long bit string (can be very large)
# print(f"Encoded Bits: {encoded_bit_string[:500]}...") # Print first 500 bits

decoded_text = decode_lzw_from_bits(encoded_bit_string)
print(f"Decoded Length: {len(decoded_text)}")
# print(f"Decoded Text: {decoded_text}")

print(f"Original == Decoded: {input_text == decoded_text}")


# Test KWK case crossing bit width boundary potentially
# This sequence might trigger interesting dictionary growth
test_kwk = "abababababababababababababababab"
print("\nTesting KWK style input:")
print(f"Original: {test_kwk}")
encoded_kwk = encode_lzw_to_bits(test_kwk)
print(encoded_kwk)
print(f"Encoded KWK Bits Length: {len(encoded_kwk)}")
decoded_kwk = decode_lzw_from_bits(encoded_kwk)
print(f"Decoded KWK: {decoded_kwk}")
print(f"KWK Original == Decoded: {test_kwk == decoded_kwk}")
