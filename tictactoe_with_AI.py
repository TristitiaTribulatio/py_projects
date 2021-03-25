from random import randrange
from math import inf


class CellOccupiedError(Exception):
    def __str__(self):
        return "This cell is occupied! Choose another one!"


class LimitationCoordinatesError(Exception):
    def __str__(self):
        return "Coordinates should be from 1 to 3!"


class NaNError(Exception):
    def __str__(self):
        return "You should enter numbers!"


class TicTacToe:
    def __init__(self, wins, first, second):
        self.X, self.O, self.move, self.wins, self.first, self.second, self.list = 0, 0, 0, wins, first, second, list()
        self.scores = {"win": 1, "lose": -1, "draw": 0}
        self.field = self.create_field("_"*9)
        self.print_field()

    def make_move(self):
        while True:
            try:
                coord = None
                if self.move % 2 == 0:
                    if self.first == "user":
                        coord = self.user_move()
                    elif self.first == "easy":
                        coord = self.easy_move()
                        if not coord:
                            continue
                    elif self.first == "medium":
                        coord = self.medium_move("X")
                    elif self.first == "hard":
                        print('Making move level "hard"')
                        coord = self.hard_move(self.field, "O")
                        coord = [coord[0], coord[1]]
                elif self.move % 2 == 1:
                    if self.second == "user":
                        coord = self.user_move()
                    elif self.second == "easy":
                        coord = self.easy_move()
                        if not coord:
                            continue
                    elif self.second == "medium":
                        coord = self.medium_move("O")
                    elif self.second == "hard":
                        print('Making move level "hard"')
                        coord = self.hard_move(self.field, "O")
                        coord = [coord[0], coord[1]]

                if self.move % 2 == 0:
                    self.field[coord[0]][coord[1]] = "X"
                elif self.move % 2 == 1:
                    self.field[coord[0]][coord[1]] = "O"

                self.print_field()
                if self.check_state(self.field, "+"):
                    break
                self.move += 1

            except CellOccupiedError as error:
                print(error)
            except LimitationCoordinatesError as error:
                print(error)
            except NaNError as error:
                print(error)

    def user_move(self):
        coord = input("Enter the coordinates: ").split()
        if not coord[0].isdigit() or not coord[1].isdigit():
            raise NaNError
        coord = list(map(int, coord))
        if not 1 <= coord[0] <= 3 or not 1 <= coord[1] <= 3:
            raise LimitationCoordinatesError
        coord = list(map(lambda x: x - 1, coord))
        if self.field[coord[0]][coord[1]] in ["X", "O"]:
            raise CellOccupiedError
        return coord

    def easy_move(self):
        coord = [randrange(0, 3), randrange(0, 3)]
        if self.field[coord[0]][coord[1]] in ["X", "O"]:
            return False
        print('Making move level "easy"')
        return coord

    def medium_move(self, state):
        if state == "X":
            return self.medium_init_coord("O", "X")
        elif state == "O":
            return self.medium_init_coord("X", "O")

    def medium_init_coord(self, x, y):
        coord = self.medium_check_win(x)
        if coord:
            return coord
        coord = self.medium_check_win(y)
        if coord:
            return coord
        while True:
            coord = [randrange(0, 3), randrange(0, 3)]
            if self.field[coord[0]][coord[1]] in ["X", "O"]:
                continue
            break
        return coord

    def medium_check_win(self, state):
        for x in range(len(self.field)):
            for y in range(len(self.field[x])):
                if self.field[x][y] in ["X", "O"]:
                    continue
                self.field[x][y] = state
                for z in self.wins:
                    if len(list(filter(lambda w: self.field[w // 3][w % 3] == state, z))) == 3:
                        return [x, y]
                self.field[x][y] = "_"
        return None

    def minimax(self, field, depth, is_max, my_state):
        if len(list(filter(lambda w: w != "_", list(field[0]+field[1]+field[2])))) == 9:
            result = self.check_state(field, "-")
            if result == my_state:
                return 10 - depth
            elif result != my_state and result is not None:
                return -10 + depth
            elif result is None:
                return 0

        if is_max:
            best_move = -inf
            for i in range(len(field)):
                for j in range(len(field[i])):
                    if field[i][j] == "_":
                        field[i][j] = my_state
                        best_move = max(best_move, self.minimax(field, depth+1, not is_max, my_state))
                        field[i][j] = "_"
            return best_move
        elif not is_max:
            best_move = inf
            for i in range(len(field)):
                for j in range(len(field[i])):
                    if field[i][j] == "_":
                        if my_state == "O":
                            field[i][j] = "X"
                        elif my_state == "X":
                            field[i][j] = "O"
                        best_move = min(best_move, self.minimax(field, depth+1, not is_max, my_state))
                        field[i][j] = "_"
            return best_move

    def hard_move(self, field, my_state):
        best_value, best_move = -inf, list([-1, -1])
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i][j] == '_':
                    field[i][j] = my_state
                    move_value = self.minimax(field, 0, False, my_state)
                    field[i][j] = "_"
                    if move_value > best_value:
                        best_move = list([i, j])
                        best_value = move_value
        return best_move

    def check_state(self, field, sign):
        for x in self.wins:
            if len(list(filter(lambda y: field[y // 3][y % 3] == "O", x))) == 3:
                if sign == "+":
                    print("O wins\n")
                return "O"
            elif len(list(filter(lambda z: field[z // 3][z % 3] == "X", x))) == 3:
                if sign == "+":
                    print("X wins\n")
                return "X"
        if self.move == 8:
            print("Draw\n")
            return "_"

    def print_field(self):
        print("-"*9)
        for ar in self.field:
            print("|", end=" ")
            for el in ar:
                print(el, end=" ")
                if el == "X":
                    self.X += 1
                elif el == "O":
                    self.O += 1
            print("|")
        print("-" * 9)

    @staticmethod
    def create_field(cells):
        field = list(map(str, cells))
        return list([field[:3], field[3:6], field[6:9]])


def main():
    wins = list([[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]])
    while True:
        command = input("Input command: ").split()
        if command[0] == "exit":
            break
        elif len(command) <= 2:
            print("Bad parameters!")
            continue
        TicTacToe(wins, command[1], command[2]).make_move()


if __name__ == "__main__":
    main()