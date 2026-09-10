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
    m_str = """16   7  20  21
                         29  12  28  17
                          1  15  23  26
                          5  18  31  10
                          2   8  24  14
                         32  27   3   9
                         19  13  30   6
                         22  11   4  25
"""
    print_matrix((parse_matrix(m_str)))


if __name__ == "__main__":
    main()