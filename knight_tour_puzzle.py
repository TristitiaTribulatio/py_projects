from numpy import array


class KnightTourPuzzle:
    def __init__(self):
        self.field, self.sign, self.knight, self.passed_moves = [], '', [], []
        self.moves, self.available_moves = [[-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, 1], [-2, -1]], []
        self.init_option('field')
        self.init_option('knight')
        while True:
            self.possible_moves('write', [self.knight[0], self.knight[1]])
            self.show_field()
            if self.check_end():
                break
            self.next_move()

    def init_option(self, init):
        while True:
            values = []
            if init == 'field':
                values = input("Enter your board dimensions: ").split()
            elif init == 'knight':
                values = input("Enter the knight's starting position: ").split()

            if self.check_values(values):
                if init == 'field':
                    self.sign = '_' * len(str(int(values[0]) * int(values[1])))
                    self.field = array([[self.sign] * int(values[0])] * int(values[1]))
                    break
                elif init == 'knight':
                    if 1 <= int(values[0]) <= len(self.field[0]) and 1 <= int(values[1]) <= len(self.field):
                        self.field[int(values[1]) - 1][int(values[0]) - 1] = (' ' * (len(self.sign) - 1)) + 'X'
                        self.knight = [int(values[1]), int(values[0])]
                        break
            if init == 'field':
                print('Invalid dimensions!')
            elif init == 'knight':
                print('Invalid position!')

    def show_field(self):
        multiplier = len(self.sign) + 1
        wall = (' ' * 2) + ('-' * (len(self.field[0]) * multiplier + 3))
        print(wall)
        for row in range(len(self.field), 0, -1):
            if row >= 10:
                print(f'{row}| ', end='')
            else:
                print(f'{" " * (len(str(len(self.field))) - 1)}{row}| ', end='')
            [print(f'{el} ', end='')for el in self.field[row-1]]
            print('|')
        print(wall + '\n' + ' ' * (len(str(len(self.field[0]))) + 1), end='')
        for num in range(1, len(self.field[0]) + 1):
            print(f'{" " * (len(self.sign) - (len(str(num)) - 1))}{num}', end='')

    def possible_moves(self, action, values):
        if action == 'check':
            if '*' not in self.field[values[0] - 1][values[1] - 1]:
                self.available_moves.append([values[0], values[1]])
        moves = 0
        for move in range(8):
            check = [values[0] + self.moves[move][0], values[1] + self.moves[move][1]]
            if 1 <= check[1] <= len(self.field[0]) and 1 <= check[0] <= len(self.field):
                if action == 'write':
                    self.field[check[0]-1][check[1]-1] = (' ' * (len(self.sign) - 1)) + str(self.possible_moves('check', [check[0], check[1]]))
                elif action == 'check':
                    if 'X' not in self.field[check[0]-1][check[1]-1] and '*' not in self.field[check[0]-1][check[1]-1]:
                        moves += 1
        if action == 'check':
            if '*' not in self.field[values[0] - 1][values[1] - 1]:
                return moves
            return '*'

    def next_move(self):
        while True:
            values = input("\nEnter your next move: ").split()
            if self.check_values(values):
                values = [int(num) for num in values]
                if values[::-1] in self.available_moves:
                    self.reset(values)
                    break
            print('Invalid move!', end='')

    def reset(self, values):
        self.field = array([[self.sign] * len(self.field[0])] * len(self.field))
        self.passed_moves.append([self.knight[1], self.knight[0]])
        for val in self.passed_moves:
            self.field[val[1] - 1][val[0] - 1] = (' ' * (len(self.sign) - 1)) + '*'
        self.field[values[1] - 1][values[0] - 1] = (' ' * (len(self.sign) - 1)) + 'X'
        self.knight = [values[1], values[0]]
        self.available_moves = []

    def check_end(self):
        if not self.available_moves:
            if [True if '*' in el else False for row in self.field for el in row].count(True) == (len(self.field[0]) * len(self.field)) - 1:
                print('\nWhat a great tour! Congratulations!')
            else:
                print(f'\nNo more possible moves!\nYour knight visited {len(self.passed_moves) + 1} squares!')
            return True
        return False

    @staticmethod
    def check_values(values):
        if len(values) == 2\
                and False not in [num.isdigit() for num in values]\
                and False not in [bool('.' not in num) for num in values]\
                and 0 not in [int(num) for num in values]:
            return True
        return False


if __name__ == '__main__':
    KnightTourPuzzle()
