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
    k_perm_i_56 = permute(master_key64, db.pc_1, lossy=True)

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
        yield permute(cd56, db.pc_2, lossy=True)

        


def flatten_nested_list(nested_list):
    return [e for sublist in nested_list for e in sublist]


def permute(bits, p_box, lossy=False):
    """takes a string of bits, and a permutation box(as a list of
    lists), and permutes the bits by the box, returning a string of
    bits. Verifies lengths are equal first unless lossy=False"""
    p_list = flatten_nested_list(p_box)
    #print(f"{str_w_len(bits)} - bits")
    #print(f"{str_w_len(p_list)} - p_list")
    if not lossy:
        assert len(p_list) == len(bits)
    else:
        assert len(p_list) <= len(bits)
    result_list = [] #turn the string of bits into a list of bits

    for old_pos in p_list:
        idx = old_pos-1
        # print(f"{bits[idx]} to {idx}. ", end="")
        result_list.append(bits[idx])

    result = ""
    for e in result_list:
        result = result + e

    return result


def main(message, key):
    plaintext = message
    subkeys = loadkeys(hex_to_bin(key))

    # Plaintext split into 64 bits
    #print(f"{plaintext} - plaintext")
    plain_as_bin = hex_to_bin(plaintext)
    #print(f"{plain_as_bin} - Plaintext split into 64 bits")
    #print(f"length of plaintext bits: {len(plain_as_bin)}")
    
    # Initial permutation IP
    perm_i = permute(hex_to_bin(plaintext), db.p_i)
    #print(f"{str_w_len(perm_i)} - perm_i")

    
    # Structure for code (blocks of 64, key of 56)
    # DES encryption - 16 rounds, different subkey each round

    for subkey48 in subkeys:
        print(f"{str_w_len(subkey48)} - subkey48") 
    # Each round:
        # Split L0 and R0 (64 --> 32, 32)
        # R0 copied to L1 (32 --> 32)
        # Key transformation (54 --> 48)      
            # details... (Learning about this on Wednesday) spits out K1 (48)
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
        # Repeat 16 times

    # One more L/R swap at the end (just a clean swap)
    # Then a final permutation IP^-1
    # Yield ciphertext


if __name__ == "__main__":
    M = "0123456789ABCDEF"
    K = "133457799BBCDFF1"
    main(M, K)