import data_boxes as db
import converter as con
import sys


def loadkeys(master_key64):
    """
    Takes a 64-bit master key and returns a generator for 16 28-bit
    subkeys
    """
    k_perm_i_56 = permute(master_key64, db.pc_1)

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

        yield permute(c28 + d28, db.pc_2)


def flatten_nested_list(nested_list):
    """Takes a list of lists and returns a flattened list"""
    return [e for sublist in nested_list for e in sublist]


def permute(bits, p_box):
    """takes a string of bits, and a permutation box(as a list of
    lists), and permutes the bits by that box, returning a string of
    permuted bits."""

    p_list = flatten_nested_list(p_box)
    result_list = []

    for old_pos in p_list:
        new_pos = old_pos-1
        result_list.append(bits[new_pos])

    return "".join(result_list)


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
    """takes 6 bits as a list and an s_box, returns a bit string corresponding to their
    evaluation"""
    row = int(bits6[0] + bits6[5], 2)
    col = int("".join(bits6[1:5]), 2)

    val = s_box[row][col]
    return f"{val:04b}"


def run_s_boxes(subsets8_6):
    """takes a list of 8 subsets of 6 bits each, puts each through the
    appropriate s box, and returns a combined string of 32 bits"""
    s_boxes = [db.s_1, db.s_2, db.s_3, db.s_4, db.s_5, db.s_6, db.s_7, db.s_8]
    s_boxes_out8_4 = []

    s_box_idx = 0
    for subset6 in subsets8_6:
        bits4 = s_box_transform(subset6, s_boxes[s_box_idx])
        s_boxes_out8_4.append(bits4)
        s_box_idx += 1
    
    return "".join(s_boxes_out8_4)


def f_box(R32, subkey48):
    """Takes the Right 32 bits and the 48 bit subkey for the round,
    and runs the f box on it, returning a new 32 bit string"""
    bits48 = xor(permute(R32, db.expand), subkey48)

    s_boxed32 = run_s_boxes(as_subsets(bits48, 6))

    return permute(s_boxed32, db.p)
    

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


def encode_DES_from_hex16(message_hex, key):
    bits64 = permute(con.hex_str_to_bin(message_hex), db.ip)
    subkeys = loadkeys(con.hex_str_to_bin(key))

    L32 = bits64[:32]
    R32 = bits64[32:]

    for subkey48 in subkeys:
        temp = R32

        f_out32 = f_box(R32, subkey48)

        R32 = xor(L32, f_out32)
        L32 = temp

    final_bits = permute(R32 + L32, db.ip_n1)

    return con.bin_str_to_hex(final_bits)


def main(argv):
    if len(argv) == 3:
        M = argv[1]
        K = argv[2]
    else:
        print("Running test data...")
        M = "0123456789ABCDEF"
        K = "133457799BBCDFF1"

    print(f"M: {M}\nK: {K}")
    ciphertext = encode_DES_from_hex16(M, K)
    print(f"C: {ciphertext}")



if __name__ == "__main__":
    main(sys.argv)

    