def parse_matrix(m:str):
    result = []

    for line in m.splitlines():
        row = []

        for num in line.split():
            row.append(int(num))

        result.append(row)

    return result

def print_matrix(matrix):
    for i in range(len(matrix)):
        row = matrix[i]
        if i == 0:
            print(f"[{row}", end="")
        else:
            print(f",\n\t{row}", end="")
    print("]")

def main():
    m_str = """40     8   48    16    56   24    64   32
            39     7   47    15    55   23    63   31
            38     6   46    14    54   22    62   30
            37     5   45    13    53   21    61   29
            36     4   44    12    52   20    60   28
            35     3   43    11    51   19    59   27
            34     2   42    10    50   18    58   26
            33     1   41     9    49   17    57   25
"""
    print_matrix((parse_matrix(m_str)))


if __name__ == "__main__":
    main()