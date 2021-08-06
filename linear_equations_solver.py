from argparse import ArgumentParser


class LinearEquationsSolver:
    def __init__(self):
        self.matrix = {'eqs': [], 'consts': []}
        self.files = self.get_args()
        self.read_file()
        self.gauss()
        print(f"The solution is: ({str(self.matrix['consts']).lstrip('[').rstrip(']')})")
        self.write_file()

    @staticmethod
    def get_args():
        parser = ArgumentParser()
        parser.add_argument('--infile', type=str)
        parser.add_argument('--outfile', type=str)
        args, list_args = parser.parse_args(), []
        for arg in vars(args):
            if getattr(args, arg) is not None:
                list_args.append(getattr(args, arg))
        return list_args

    def read_file(self):
        with open(self.files[0], 'r') as file:
            num_eq = int(file.readline())
            for _ in range(num_eq):
                eq = [float(num) for num in file.readline().split()]
                self.matrix['eqs'].append(eq[:len(eq) - 1])
                self.matrix['consts'].append(eq[-1])

    def gauss(self):
        print('Start solving the equation.')
        for row in range(len(self.matrix['eqs'])):
            self.divided_row(row)
            if row < len(self.matrix['eqs']) - 1:
                self.combine_rows(row, row + 1, len(self.matrix['eqs']), 1)
        for row in range(len(self.matrix['eqs']) - 1, 0, -1):
            if row:
                self.combine_rows(row, row - 1, -1, -1)
        

    def divided_row(self, row):
        coef = round(1 / self.matrix['eqs'][row][row], 3)
        print(f"{round(coef, 1)} * R{row + 1} -> R{row + 1}")
        self.matrix['eqs'][row] = [round(num * coef, 2) for num in self.matrix['eqs'][row]]
        self.matrix['consts'][row] = round(self.matrix['consts'][row] * coef, 2)

    def combine_rows(self, row, start, stop, step):
        for zero in range(start, stop, step):
            multiplier = -self.matrix['eqs'][zero][row]
            self.matrix['eqs'][zero] = [round((a * multiplier) + b, 2) for a, b in zip(self.matrix['eqs'][row], self.matrix['eqs'][zero])]
            self.matrix['consts'][zero] = round((self.matrix['consts'][row] * multiplier) + self.matrix['consts'][zero], 2)
            print(f'{multiplier} * R{row + 1} + R{zero + 1} -> R{zero + 1}')

    def write_file(self):
        with open(self.files[1], 'w') as file:
            [file.write(f'{el}\n') for el in self.matrix['consts']]
        print('Saved to out.txt')
        

if __name__ == '__main__':
    LinearEquationsSolver()
