import sys
import converter as con
import functions as fn
import data_boxes as bxs



def back_round(lft, rht):
    print("MADE IT THIS FAR!!! :)")
    assert 0


def decode_DES_from_hex16(cipher_hex, key):
    keys = fn.loadkeys_list(key)
    """
    for n, k in enumerate(keys):
        print(f"{n}:\t{k}")
    """
    print(f"number of subkeys: {len(keys)}")

    bits64 = con.hex_str_to_bin(cipher_hex)
    print(bits64)
    permut1 = fn.back_permute(bits64, bxs.ip_n1)
    print(permut1)

    R32 = permut1[:32]
    L32 = permut1[32:]
    print(f"{L32} {R32}")

    for subkey in keys:
        back_round(lft=R32, rht=L32)
    



    # back_p1_inverse = backpermute(bits_64, db.ip_n1)


    return False



def main(argv):
    if len(argv) == 3:
        C = argv[1]
        K = argv[2]
    else:
        print("Running test data...")
        C = "85E813540F0AB405"
        K = "133457799BBCDFF1"

    print(f"C: {C}\nK: {K}")
    message = decode_DES_from_hex16(C, K)
    print(f"C: {message}")



if __name__ == "__main__":
    main(sys.argv)