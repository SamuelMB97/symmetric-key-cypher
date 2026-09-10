import data_boxes as db


def str_w_len(bits:str):
    return f"{bits} length: {len(bits)}"


def hex_to_bin(hex:str):
    new_length = len(hex) * 4
    return format(int(hex, 16), f"0{new_length}b")

def bin_to_hex(bin:str):
    new_length = len(bin) // 4
    return format(int(bin, 2), f"0{new_length}X")

    
def loadkeys(master_key64):
    """
    Takes a 64-bit master key and returns a generator for 16 28-bit
    subkeys
    """
    k_perm_i_56 = permute(master_key64, db.pc_1, change_size=True)

    c28 = k_perm_i_56[:28]
    d28 = k_perm_i_56[28:]

    def rotate_left(side):
        return side[1:] + side[0]
    
    for round in [n+1 for n in range(16)]:
        rotate_by = 2
        if round in [1, 2, 9, 16]:
            rotate_by = 1

        for _ in range(rotate_by):
            c28 = rotate_left(c28)
            d28 = rotate_left(d28)

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
    bits48 = xor(bits48, subkey48)
    print(f"{str_w_len(bits48)} - bits48")

    subsets8_6 = as_subsets(bits48, 6)

    s_boxed32 = run_s_boxes(subsets8_6)
    print(f"{str_w_len(s_boxed32)} - s_boxed32")

    f_out32 = permute(s_boxed32, db.p)
    print(f"{str_w_len(f_out32)} - f_out32")

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

    # Plaintext split into 64 bits and...
    # Initial permutation IP
    bits64 = permute(hex_to_bin(message_hex), db.p_i)
    #print(f"{str_w_len(perm_i)} - perm_i")

    
    # Structure for code (blocks of 64, key of 56)
    # DES encryption - 16 rounds, different subkey each round

    subkeys = loadkeys(hex_to_bin(key))

    # Each round:
    round_num = 0
    for subkey48 in subkeys:
        round_num += 1
        print(f"Round number: {round_num}")
        print(f"{str_w_len(subkey48)} - subkey48") 
    
        # Split L0 and R0 (64 --> 32, 32)
        L32_i = bits64[:32]
        R32_i = bits64[32:]

        # R0 copied to L1 (32 --> 32)
        L32_f = R32_i

        f_out32 = f_box(R32_i, subkey48)
        R32_f = xor(L32_i, f_out32)
        print("did f_box and xor...")
        print("MADE IT THIS FAR! :)")
        assert 0
        # f_box with R0 and K1 (32, 48)
            # expansion (32 --> 48)
            # EXOR with K1 (48, 48 --> 48)
            # split output from exor into 8 groups of 6
            # each 6 bits goes through a different s_box (8x(6 --> 4))
            # put them back together, (8x6 --> 32)
            # Permute them (matrix for that)
            # spits out 32
        # XOR with L0 and output from f_box (32, 32 --> 32)
            # This becomes R1 (32)
        # R0 copied to L1 (32 --> 32) (if it wasn't done before...)
        # Repeat 16 times

    # One more L/R swap at the end (just a clean swap)
    # Then a final permutation IP^-1
    # Yield ciphertext


if __name__ == "__main__":
    M = "0123456789ABCDEF"
    K = "133457799BBCDFF1"
    main(M, K)