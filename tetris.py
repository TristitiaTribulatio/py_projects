from numpy import array, amax, delete, insert


class Tetris:
    def __init__(self, width, height, dict_fields):
        self.width, self.height, self.dict_fields, self.piece = width, height, dict_fields, None
        self.empty_field = array([["-"]*self.width]*self.height)
        self.field = self.copy_field(self.empty_field)
        self.offset = {"row": 0, "column": 0, "rotate": 0}
        self.print_field(self.field)
        self.move_piece(input())

    def print_field(self, field):
        count = 0
        print("\n", end="")
        for ar in field:
            for el in ar:
                count += 1
                if count % self.width == 0:
                    print(el, end="")
                    continue
                print(el, end=" ")
            print("\n", end="")

    def filling_field(self):
        for el in self.dict_fields[self.piece][self.offset["rotate"] % len(self.dict_fields[self.piece])]:
            el += self.offset["row"] + self.offset["column"]
            self.field[el // self.width][el % self.width] = "0"
        self.print_field(self.field)

    def move_piece(self, act):
        for column in range(self.width):
            game_over = 0
            for row in self.field:
                if row[column] == "0":
                    game_over += 1
            if game_over == self.height:
                self.print_field(self.field)
                print("\nGame Over!")
                return True
        if act == "break":
            for row in range(len(self.field)):
                if len(list(filter(lambda x: x == "0", self.field[row]))) == len(self.field[row]):
                    self.field = delete(self.field, row, axis=0)
                    self.field = insert(self.field, 0, "-", axis=0)
                    self.empty_field = self.copy_field(self.field)
                if row + 1 == self.height:
                    self.print_field(self.field)
                    return None
        if act == "piece":
            self.piece = input()
            self.empty_field = self.copy_field(self.field)
            self.offset = {"row": 0, "column": 0, "rotate": 0}
        self.field = self.copy_field(self.empty_field)

        piece_position = self.dict_fields[self.piece][self.offset["rotate"] % len(self.dict_fields[self.piece])]
        end_condition = amax(piece_position) + self.offset["row"] + self.offset["column"] + self.width\
                             < self.width * self.height
        left_condition = list(filter(lambda el: el % self.width == 0,
                                     piece_position + self.offset["row"] + self.offset["column"]))
        right_condition = list(filter(lambda el: (el % self.width) % (self.width - 1) == 0 and el % self.width != 0,
                                      piece_position + self.offset["row"] + self.offset["column"]))
        for el in piece_position + self.offset["row"] + self.offset["column"]:
            if not right_condition and self.field[(el + 1) // self.width][(el + 1) % self.width] == "0":
                right_condition = True
            if not left_condition and self.field[(el - 1) // self.width][(el - 1) % self.width] == "0":
                left_condition = True
            if end_condition and not right_condition\
                and self.field[(el + self.width + 1) // self.width][(el + self.width + 1) % self.width] == "0":
                right_condition = True
            if end_condition and not left_condition\
                and self.field[(el + self.width - 1) // self.width][(el + self.width - 1) % self.width] == "0":
                left_condition = True
            if end_condition and self.field[(el + self.width) // self.width][(el + self.width) % self.width] == "0":
                end_condition = False
        if end_condition:
            if act == "left" and not bool(left_condition):
                self.offset["column"] -= 1
                self.offset["row"] += self.width
            elif act == "right" and not bool(right_condition):
                self.offset["column"] += 1
                self.offset["row"] += self.width
            elif act == "rotate" and not bool(left_condition) and not bool(right_condition):
                self.offset["rotate"] += 1
                self.offset["row"] += self.width
            elif act == "down":
                self.offset["row"] += self.width
            right_condition, left_condition = False, False
        self.filling_field()

    @staticmethod
    def copy_field(field):
        return array(field)


def main():
    width, height = map(int, input().split())
    dict_fields = {"O": array([[4, 14, 15, 5]]),
                   "I": array([[4, 14, 24, 34], [3, 4, 5, 6]]),
                   "S": array([[5, 4, 14, 13], [4, 14, 15, 25]]),
                   "Z": array([[4, 5, 15, 16], [5, 15, 14, 24]]),
                   "L": array([[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]),
                   "J": array([[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]),
                   "T": array([[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]])}
    tetris = Tetris(width, height, dict_fields)
    while True:
        user_input = input()
        if user_input == "exit":
            break
        if tetris.move_piece(user_input):
            break


if __name__ == "__main__":
    main()
