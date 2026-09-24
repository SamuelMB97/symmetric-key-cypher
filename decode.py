import sys
import converter as con
import functions as fn
import data_boxes as bxs



def decode_DES_from_hex16(cipher_hex, key):
    bits64 = con.hex_str_to_bin(cipher_hex)
    print(bits64)
    forward = fn.permute(bits64, bxs.ip)
    #print(forward)
    #andback = fn.permute(forward, bxs.ip_n1)
    andback = fn.back_permute(forward, bxs.ip)
    print(andback)


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