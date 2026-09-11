import data_boxes as db
import numbersystem
import converter as con

def str_w_len(bits:str):
    length = len(bits)
    bits_list = [b for b in bits]
    new_len = int((length / 4) * 5)
    for n in range(4, new_len, 5):
        bits_list.insert(n, " ")

    as_str = "".join(bits_list)
    return f"{as_str} length: {length}"


def hex_to_bin(hex:str):
    #print(f"{hex} - hex")

    new_length = len(hex) * 4
    #print(f"{new_length} - new_length")
    
    return numbersystem.hexaToBinary(hex).rjust(new_length, '0')
    print(f"{numbersystem.hexaToBinary(hex).rjust(new_length, '0')} new to Bin")

    a = int(hex, 16)
    #print(f"{a} - integer")

    b = format(a, f"0{new_length}b")
    #print(f"{str_w_len(b)} - binary")
    print(format(int(hex, 16), f"0{new_length}b"))

    return format(int(hex, 16), f"0{new_length}b")

def bin_to_hex(bin:str):
    new_length = len(bin) // 4
    return numbersystem.binaryToHexa(bin).rjust(new_length, '0')
    print(f"{numbersystem.binaryToHexa(bin).rjust(new_length, '0')} new to Hex")
    print(format(int(bin, 2), f"0{new_length}X"))
    return format(int(bin, 2), f"0{new_length}X")

    
def loadkeys(master_key64):
    """
    Takes a 64-bit master key and returns a generator for 16 28-bit
    subkeys
    """
    #print(f"{str_w_len(master_key64)} - Key as bin")
    k_perm_i_56 = permute(master_key64, db.pc_1, change_size=True)

    #print(f"{str_w_len(k_perm_i_56)} - k_perm_i_56")


    c28 = k_perm_i_56[:28]
    d28 = k_perm_i_56[28:]

    #print(f"{str_w_len(c28)} - c28")
    #print(f"{str_w_len(d28)} - d28")


    def rotate_left(side):
        return side[1:] + side[0]
    
    for round in [n+1 for n in range(16)]:
        rotate_by = 2
        if round in [1, 2, 9, 16]:
            rotate_by = 1

        for _ in range(rotate_by):
            c28 = rotate_left(c28)
            d28 = rotate_left(d28)

        #print(f"{str_w_len(c28)} - C")
        #print(f"{str_w_len(d28)} - D")

        cd56 = c28 + d28
        yield permute(cd56, db.pc_2, change_size=True)


def flatten_nested_list(nested_list):
    return [e for sublist in nested_list for e in sublist]


def permute(bits, p_box, change_size=False):
    """takes a string of bits, and a permutation box(as a list of
    lists), and permutes the bits by the box, returning a string of
    bits. Verifies lengths are appropriate according to change_size"""
    p_list = flatten_nested_list(p_box)

    #print(f"{str_w_len(bits)} - bits")
    #print(f"{str_w_len(p_list)} - p_list")

    if not change_size:
        assert len(p_list) == len(bits)
    else:
        assert len(p_list) != len(bits)
    result_list = [] #turn the string of bits into a list of bits

    for old_pos in p_list:
        new_pos = old_pos-1
        # print(f"{bits[new_pos]} to {new_pos}. ", end="")
        result_list.append(bits[new_pos])

    return "".join(result_list)

    result = ""
    for e in result_list:
        result = result + e

    return result


def as_subsets(bits, num_sets):
    """
    Takes a string of bits and returns it as a list of lists with
    length = num_sets
    """
    subsets = []

    for i in range(0, len(bits), num_sets): # get 8 subsets of 6 from the bits
        subsets.append([bits[i+j] for j in range(6)])

    return subsets


def s_box_transform(bits6:list, s_box):
    row = int(bits6[0] + bits6[5], 2)
    col = int("".join(bits6[1:5]), 2)

    val = s_box[row][col]
    bits4 = f"{val:04b}"
    # print(f"row: {row}, col: {col}, val = {val}, as binary: {bits4}")
    return bits4


def run_s_boxes(subsets8_6):
    s_box_idx = 0
    s_boxes = [db.s_1, db.s_2, db.s_3, db.s_4, db.s_5, db.s_6, db.s_7, db.s_8]
    s_boxes_out8_4 = []

    for subset6 in subsets8_6:
        # print(f"{subset6}, AND {s_box_idx}")
        bits4 = s_box_transform(subset6, s_boxes[s_box_idx])
        s_boxes_out8_4.append(bits4)
        s_box_idx += 1
    
    return "".join(s_boxes_out8_4)


def f_box(R32, subkey48):
    bits48 = permute(R32, db.expand, change_size=True)
    #print(f"{str_w_len(bits48)} - bits48")

    bits48 = xor(bits48, subkey48)
    #print(f"{str_w_len(bits48)} - bits48")

    subsets8_6 = as_subsets(bits48, 6)

    s_boxed32 = run_s_boxes(subsets8_6)
    #print(f"{str_w_len(s_boxed32)} - s_boxed32")

    f_out32 = permute(s_boxed32, db.p)
    #print(f"{str_w_len(f_out32)} - f_out32")

    return f_out32
    

def xor(a, b):
    """Takes 2 strings of equal length (in binary), returns xor string"""
    length = len(a)
    assert len(b) == length

    result = []
    for i in range(length):
        if a[i] != b[i]:
            result.append("1")
        else:
            result.append("0")

    return "".join(result)



def main(message_hex, key):
    #print(message_hex)

    as_bin = con.hex_str_to_bin(message_hex)

    print(f"{str_w_len(as_bin)} - bits48 init")
    # Plaintext split into 64 bits and...
    # Initial permutation IP
    bits64 = permute(as_bin, db.ip)
    print("IP(M) = 14A7D67818CA18AD reference")
    print(f"IP(M) = {con.bin_str_to_hex(bits64)} what I got")
    print()
    print(f"{str_w_len(con.hex_str_to_bin("14A7D67818CA18AD"))}")
    print(f"{str_w_len(con.bin_str_to_hex(bits64))}")
    print()
    #print(f"{str_w_len(bits64)} - bits64 initial perm.")

    
    # Structure for code (blocks of 64, key of 56)
    # DES encryption - 16 rounds, different subkey each round

    subkeys = loadkeys(con.hex_str_to_bin(key))

    # Split L0 and R0 (64 --> 32, 32)
    L32 = bits64[:32]
    R32 = bits64[32:]
    
    print("L0 = 14A7D678 REFERENCE")
    print(f"L0 = {con.bin_str_to_hex(L32)}")
    print()
    print("R0 = 18CA18AD REFERENCE")
    print(f"R0 = {con.bin_str_to_hex(R32)}")
    print()
    
    # Each round:
    round_num = 0
    for subkey48 in subkeys:

        print("K1 = 1B02EFFC7072")
        print(f"K1 = {con.bin_str_to_hex(subkey48)}")
        print()

        #print(f"{str_w_len(subkey48)} - subkey48")
        round_num += 1
        #print(f"Round number: {round_num}")
        #print(f"{str_w_len(subkey48)} - subkey48") 
    
        #print(f"{str_w_len(L32)} - L32") 
        #print(f"{str_w_len(R32)} - R32") 


        # R0 copied to L1 (32 --> 32)
        L32_next = R32

        #print(f"{str_w_len(L32)} - L32") 

        f_out32 = f_box(R32, subkey48)

        R32 = xor(L32, f_out32)#f_box(R32, subkey48))

        #print(f"{str_w_len(R32)} - R32") 

        L32 = L32_next
        #print(f"{str_w_len(L32)} - L32") 
        #print(f"{str_w_len(R32)} - R32") 
        
        print("L1 = 18CA18AD")
        print(f"L1 = {con.bin_str_to_hex(L32)}")
        print()
        print("R1 = 5A78E394")
        print(f"R1 = {con.bin_str_to_hex(R32)}")
        print()

        #assert 0

        # Repeat 16 times

    # One more L/R swap at the end (just a clean swap)
    swapped64 = R32 + L32
    #print(f"{str_w_len(swapped64)} - swapped64")
    # Then a final permutation IP^-1
    final_bits = permute(swapped64, db.ip_n1)
    #print(f"{str_w_len(final_bits)} - final_bits")

    # Yield ciphertext
    ciphertext = con.bin_str_to_hex(final_bits)
    print(f"C = {ciphertext}")


if __name__ == "__main__":
    tests = [
        ["0123456789ABCDEF",
         "133457799BBCDFF1"],
        ["0000000000000000",
         "0000000000000000"],
        ["FFFFFFFFFFFFFFFF",
         "FFFFFFFFFFFFFFFF"],
        ["0123456789ABCDEF",
         "133457799BBCDFF1"],
        ["1234567890ABCDEF",
         "133457799BBCDFF1"],
        ["FEDCBA9876543210",
         "133457799BBCDFF1"]
    ]
    the_test = 5
    if the_test:
        print(f"M = {tests[the_test-1][0]}\nK = {tests[the_test-1][1]}")
        main(tests[the_test-1][0], tests[the_test-1][1])
    else:
        for test in tests:
            print(f"M = {test[0]}\nK = {test[1]}")
            main(test[0], test[1])
            print()