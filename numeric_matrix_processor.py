import numpy
m1, m2, res_m, r_c = list(), list(), list(), list([['r1', 0], ['c1', 0], ['r2', 0], ['c2', 0]])


def init_matrix(quan_of_m):
    global m1, m2, r_c
    if quan_of_m == "2":

        r_c[0][1], r_c[1][1] = input("Enter size of first matrix: ").split()
        print("Enter first matrix: ")
        for j in range(int(r_c[0][1])):
            m1.append(input().split())

        r_c[2][1], r_c[3][1] = input("Enter size of second matrix: ").split()
        print("Enter second matrix: ")
        for j in range(int(r_c[2][1])):
            m2.append(input().split())

        for i in range(len(m1)):
            for j in range(len(m1[i])):
                m1[i][j] = float(m1[i][j])

        for i in range(len(m2)):
            for j in range(len(m2[i])):
                m2[i][j] = float(m2[i][j])

    elif quan_of_m == "1":

        r_c[0][1], r_c[1][1] = input("Enter size of matrix: ").split()
        print("Enter matrix:")
        for j in range(int(r_c[0][1])):
            m1.append(input().split())

        for i in range(len(m1)):
            for j in range(len(m1[i])):
                m1[i][j] = float(m1[i][j])


def check_correct():
    global r_c
    if r_c[0][1] == r_c[2][1] and r_c[1][1] == r_c[3][1]:
        return True
    else:
        return False


def print_matrix(act):
    global res_m, r_c
    print("The result is:")
    for i in range(int(r_c[0][1])):
        if act == "0":
            print(str(res_m[i]).lstrip("[").rstrip("]").replace(",", ""))
        elif act == "1":
            print(str(res_m[i]).lstrip("[").rstrip("]"))
    print("\n")
    zero_m()


def zero_m():
    global res_m, r_c, m1, m2
    m1, m2, res_m, r_c = list(), list(), list(), list([['r1', 0], ['c1', 0], ['r2', 0], ['c2', 0]])


def sum_matrix():
    global res_m, r_c, m1, m2
    for i in range(int(r_c[0][1])):
        res_m.append([])
        for j in range(int(r_c[1][1])):
            res_m[i].append(float(m1[i][j]) + float(m2[i][j]))


def mul_matrix_by_num(num):
    global res_m, r_c, m1
    for i in range(int(r_c[0][1])):
        res_m.append([])
        for j in range(int(r_c[0][1])):
            res_m[i].append(float(m1[i][j]) * num)


def mul_matrix():
    global res_m, r_c, m1, m2
    res_m = numpy.dot(m1, m2)


def transpose_matrix(state):
    global res_m, m1
    init_matrix("1")
    if state == "main":
        res_m = numpy.transpose(m1)
    elif state == "side":
        m1 = ([i[::-1] for i in m1])[::-1]
        res_m = numpy.transpose(m1)
    elif state == "vertical":
        res_m = [i[::-1] for i in m1]
    elif state == "horizontal":
        res_m = m1[::-1]
    print_matrix("0")


def matrix_action(act):
    init_matrix("2")
    if act == "add":
        if not check_correct():
            print("The operation cannot be performed.\n")
            return True
        sum_matrix()
        print_matrix("0")
    elif act == "mul":
        mul_matrix()
        print_matrix("1")


def multiplication_by_number():
    init_matrix("1")
    num = float(input("Enter constant: "))
    mul_matrix_by_num(num)
    print_matrix("0")


def transpose_menu():
    print("\n1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line")
    choice = int(input("Your choice: "))
    if choice == 1:
        transpose_matrix("main")
    elif choice == 2:
        transpose_matrix("side")
    elif choice == 3:
        transpose_matrix("vertical")
    elif choice == 4:
        transpose_matrix("horizontal")


def calculate_determinant():
    global res_m, m1
    init_matrix("1")
    print("The result is:\n{0}\n".format(round(numpy.linalg.det(m1), 2)))
    zero_m()


def inverse_matrix():
    global res_m, m1
    init_matrix("1")
    res_m = numpy.linalg.inv(m1)
    print_matrix("0")


def main():
    while True:
        print("1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices\n"
              "4. Transpose matrix\n5. Calculate a determinant\n6. Inverse matrix\n0. Exit")
        choice = int(input("Your choice: "))
        if choice == 1:
            matrix_action("add")
        elif choice == 2:
            multiplication_by_number()
        elif choice == 3:
            matrix_action("mul")
        elif choice == 4:
            transpose_menu()
        elif choice == 5:
            calculate_determinant()
        elif choice == 6:
            inverse_matrix()
        elif choice == 0:
            break


main()
