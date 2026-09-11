
HEX_BIN = [("0", "0000"), ("1", "0001"), ("2", "0010"), ("3", "0011"), 
           ("4", "0100"), ("5", "0101"), ("6", "0110"), ("7", "0111"), 
           ("8", "1000"), ("9", "1001"), ("A", "1010"), ("B", "1011"), 
           ("C", "1100"), ("D", "1101"), ("E", "1110"), ("F", "1111")]


def hex_to_bin(h):
    assert len(h) == 1
    for tup in HEX_BIN:
        if tup[0] == h:
            return tup[1]
    print(f"Can't find hex: {h}")
    return ValueError("Given hex not found")

def bin_to_hex(bits4):
    assert len(bits4) == 4
    for tup in HEX_BIN:
        if tup[1] == bits4:
            return tup[0]
    print(f"Can't find bit code: {bits4}")
    return ValueError("Bit code not found")

def check_atomic_conversions():
    Hex = ["0", "1", "2", "3", 
           "4", "5", "6", "7", 
           "8", "9", "A", "B", 
           "C", "D", "E", "F"]
    
    Bin = ["0000", "0001", "0010", "0011", 
           "0100", "0101", "0110", "0111",
           "1000", "1001", "1010", "1011", 
           "1100", "1101", "1110", "1111"]
    
    for hex in Hex:
        print(f"{hex}: {hex_to_bin(hex)}")
    print()

    for bin in Bin:
        print(f"{bin}: {bin_to_hex(bin)}")


def hex_str_to_bin(hex_str):
    return "".join([hex_to_bin(char) for char in hex_str])

def bin_str_to_hex(bin_str):
    bin_list = [c for c in bin_str]
    hex_list = []
    while bin_list:
        hex_list.append(bin_to_hex("".join(bin_list[:4])))
        bin_list = bin_list[4:]
    return "".join(hex_list)

def check_str_conversions():
    hex_str = ["A", "AA", "5", "123", "FC3", "01"]
    for hstr in hex_str:
        print(f"{hstr}: {hex_str_to_bin(hstr)}")
    print("hex_str_to_bin complete")

    bin_str = ["0000", "00000000", "10101010", "000111000011", "111111111111", "0110"]
    for bstr in bin_str:
        print(f"{bstr}: {bin_str_to_hex(bstr)}")
    print("bin_str_to_hex complete")


def bits_readable(bits, gap=4):
    bits_list = [b for b in bits]
    new_len = int((len(bits) / gap) * (gap+1))
    for n in range(gap, new_len, gap+1):
        bits_list.insert(n, " ")
    return "".join(bits_list)

def check_bits_readable():
    a = "111101010010001010010011"

    print(bits_readable(a))
    print(bits_readable(a, 6))


