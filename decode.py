import sys
import converter as con
import functions as fn
import data_boxes as db



def back_round(subkey, lft, rht):
    bits32 = fn.f_box(rht, subkey)
    new_prevL32 = fn.xor(bits32, lft)
    return (new_prevL32, rht)



def decode_DES_from_hex16(cipher_hex, key):
    keys = fn.loadkeys_list(key)

    bits64 = con.hex_str_to_bin(cipher_hex)
    permut1 = fn.back_permute(bits64, db.ip_n1)

    R32 = permut1[:32]
    L32 = permut1[32:]

    for subkey in reversed(keys):
        L32, R32 = back_round(subkey, lft=R32, rht=L32)

    decoded = fn.permute(L32+R32, db.ip_n1)

    return con.bin_str_to_hex(decoded)



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
    print(f"M: {message}")



if __name__ == "__main__":
    main(sys.argv)