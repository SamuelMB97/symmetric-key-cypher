import data_boxes as bxs
import converter as con


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

def back_permute(bits, p_box):

    p_list = flatten_nested_list(p_box)
    result_list = [0 for _ in range(len(p_list))]

    for i in range(len(bits)):
        new_pos = p_list[i] - 1
        result_list[new_pos] = bits[i]

    return "".join(result_list)


def loadkeys(master_key64):
    """
    Takes a 64-bit master key and returns a generator for 16 28-bit
    subkeys
    """
    k_perm_i_56 = permute(master_key64, bxs.pc_1)

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

        yield permute(c28 + d28, bxs.pc_2)


def loadkeys_list(master_key64):
    key_generator = loadkeys(con.hex_str_to_bin(master_key64))
    all_the_keys = []
    for subkey in key_generator:
        all_the_keys.append(subkey)

    return all_the_keys