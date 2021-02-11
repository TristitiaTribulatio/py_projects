wins = [[0,0, 0,1, 0,2], [1,0, 1,1, 1,2], [2,0, 2,1, 2,2], [0,0, 1,0, 2,0], [0,1, 1,1, 2,1], [0,2, 1,2, 2,2], [0,0, 1,1, 2,2], [0,2, 1,1, 2,0]]
check_x, check_o, check_draw, check_winner, player = 0, 0, 0, [], 0
e_c = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]


def tictactoe():
    global check_x, check_o

    print_field()
    while True:
        step_player()
        print_field()

        # if impossible(None):
        #     return True
        # check_x, check_o = 0, 0

        finish = check_win()
        if finish:
            break
    # if not finish:
    #     print("Game not finished")


def draw():
    global check_draw
    check_draw += 1
    if check_draw == 9:
        print("Draw")
        return True
    else:
        return False


def impossible(check):
    global check_x, check_o
    for i in range(len(e_c)):
        for j in range(3):
            if e_c[i][j] == "X":
                check_x += 1
            elif e_c[i][j] == "O":
                check_o += 1
    if abs(check_x - check_o) >= 2 or check == "true":
        print("Impossible")
        return True
    return False


def check_win():
    global check_x, check_o, check_winner

    for i in range(len(wins)):
        for j in range(0, len(wins[i]), 2):
             if e_c[wins[i][j]][wins[i][j + 1]] == "X":
                check_x += 1
                if check_x == 3:
                    check_winner.append("X")
             else:
                 check_x = 0

             if e_c[wins[i][j]][wins[i][j + 1]] == "O":
                 check_o += 1
                 if check_o == 3:
                     check_winner.append("O")
             else:
                 check_o = 0
        check_o, check_x = 0, 0

    if len(check_winner) == 1:
        print("{0} wins".format(check_winner[0]))
        return True
    # elif len(check_winner) == 2:
    #     impossible("true")
    #     return True
    elif draw():
        return True
    return False


def step_player():
    global e_c, player
    while True:
        step = list(input("Enter the coordinates: ").split())
        if step[0] not in "1234567890" or step[1] not in "1234567890":
            print("You should enter numbers!")
            continue
        step[0], step[1] = int(step[0]), int(step[1])
        if step[0] > 3 or step[0] < 1 or step[1] > 3 or step[1] < 1:
            print("Coordinates should be from 1 to 3!")
            continue
        if e_c[step[0] - 1][step[1] - 1] == "X" or e_c[step[0] - 1][step[1] - 1] == "O":
            print("This cell is occupied! Choose another one!")
            continue

        if player % 2 == 0:
            e_c[step[0] - 1][step[1] - 1] = "X"
        else:
            e_c[step[0] - 1][step[1] - 1] = "O"
        player += 1

        break


def print_field():
    print("------------")
    print(f"| {e_c[0][0]} {e_c[0][1]} {e_c[0][2]} |")
    print(f"| {e_c[1][0]} {e_c[1][1]} {e_c[1][2]} |")
    print(f"| {e_c[2][0]} {e_c[2][1]} {e_c[2][2]} |")
    print("------------")


tictactoe()