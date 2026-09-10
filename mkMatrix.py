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
    m_str = """57   49    41   33    25    17    9
               1   58    50   42    34    26   18
              10    2    59   51    43    35   27
              19   11     3   60    52    44   36
              63   55    47   39    31    23   15
               7   62    54   46    38    30   22
              14    6    61   53    45    37   29
              21   13     5   28    20    12    4
"""
    print_matrix((parse_matrix(m_str)))


if __name__ == "__main__":
    main()