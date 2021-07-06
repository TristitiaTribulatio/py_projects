from random import randint


class GeneratingRandomness:
    def __init__(self):
        self.string, self.prediction = '', ''
        self.statistics = {f'{i}{j}{k}': [0, 0] for i in range(2) for j in range(2) for k in range(2)}
        self.enter_string()

    def enter_string(self):
        MIN_LENGTH = 100
        print("Please give AI some data to learn...\nThe current data length is 0, 100 symbols left")
        while True:
            string = input("Print a random string containing 0 or 1:\n\n")
            for sym in string:
                if sym in ['0', '1']:
                    self.string += sym
            if MIN_LENGTH - len(self.string) <= 0:
                break
            print(f"Current data length is {len(self.string)}, {MIN_LENGTH - len(self.string)} symbols left")
        print(f'\nFinal data string:\n{self.string}\n')
        self.analyzing_string()

    def analyzing_string(self):
        start, end = 0, 3
        for _ in range(len(self.string) - 3):
            if self.string[end] == '1':
                self.statistics[self.string[start:end]][1] += 1
            elif self.string[end] == '0':
                self.statistics[self.string[start:end]][0] += 1
            start += 1
            end += 1
        self.enter_test_string()

    def enter_test_string(self):
        print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.""")
        print("""Otherwise, you earn $1. Print "enough" to leave the game. Let's go!""")
        money = 1000
        while True:
            s = input("\nPrint a random string containing 0 or 1:\n")
            if s == 'enough':
                print("Game over!")
                break
            elif s.isdigit():
                for j in range(3):
                    self.prediction += str(randint(0, 1))
                for i in range(len(s)-3):
                    triad = [int(num) for num in self.statistics[s[i:i+3]]]
                    self.prediction += '0' if triad[0] >= triad[1] else '1'
                print(f"prediction:\n{self.prediction}\n")
                coincidence = 0
                for i in range(3, len(self.prediction)):
                    if s[i] == self.prediction[i]:
                        coincidence += 1
                money = money - coincidence + ((len(s) - 3) - coincidence)
                self.prediction = ''
                print(f'Computer guessed right {coincidence} out of {len(s) - 3} symbols ({round((coincidence / (len(s) - 3)) * 100, 2)} %)')
                print(f'Your capital is now ${money}')


if __name__ == "__main__":
    GeneratingRandomness()
