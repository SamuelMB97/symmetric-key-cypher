


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


