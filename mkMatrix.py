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
    m_str = """   14    17   11    24     1    5
                  3    28   15     6    21   10
                 23    19   12     4    26    8
                 16     7   27    20    13    2
                 41    52   31    37    47   55
                 30    40   51    45    33   48
                 44    49   39    56    34   53
                 46    42   50    36    29   32
"""
    print_matrix((parse_matrix(m_str)))


if __name__ == "__main__":
    main()