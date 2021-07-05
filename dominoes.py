from random import randint, choice
from operator import itemgetter


class Dominoes:
    def __init__(self):
        self.dominoes_set, self.player_pieces, self.computer_pieces = [], [], []
        self.stock_pieces, self.status, self.field = [], '', []
        self.snake_bellow = {f'{i}': 0 for i in range(7)}
        self.create_set(False)
        
    def create_set(self, redistribution):
        if redistribution:
            self.player_pieces, self.computer_pieces, self.stock_pieces = [], [], []
        [self.dominoes_set.append([i, j]) for i in range(7) for j in range(i, 7)]
        self.split_set()

    def split_set(self):
        for _ in range(len(self.dominoes_set)):
            piece = randint(0, len(self.dominoes_set)-1)
            if len(self.player_pieces) < 7:
                self.player_pieces.append(self.dominoes_set[piece])
            elif len(self.computer_pieces) < 7:
                self.computer_pieces.append(self.dominoes_set[piece])
            else:
                self.stock_pieces.append(self.dominoes_set[piece])
            del self.dominoes_set[piece]
        self.determine_piece_and_player()

    def determine_piece_and_player(self):
        player_snake = [['computer', piece[0]] for piece in self.player_pieces if piece[0] == piece[1]]
        computer_snake = [['player', piece[0]] for piece in self.computer_pieces if piece[0] == piece[1]]
        if player_snake+computer_snake == []:
            self.create_set(True)
        start_piece = sorted(player_snake+computer_snake, key=itemgetter(1))[-1]
        self.status = start_piece[0]
        domino_snake = [[start_piece[1]] * 2]
        if self.status == 'computer':
            del self.player_pieces[self.player_pieces.index(domino_snake[0])]
        elif self.status == 'player':
            del self.computer_pieces[self.computer_pieces.index(domino_snake[0])]
        self.field.append(domino_snake[0])
        self.snake_bellow[str(domino_snake[0][0])] += 2
        self.show_move()

    def show_move(self):
        print('='*70 + f'\nStock size: {len(self.stock_pieces)}\nComputer pieces: {len(self.computer_pieces)}\n\n')
        if len(self.field) <= 6:
            [print(piece, end='') for piece in self.field]
        else:
            f = self.field
            print(f'{f[0]}{f[1]}{f[2]}...{f[-3]}{f[-2]}{f[-1]}')
        print('\n\nYour pieces:')
        [print(f'{piece+1}:{self.player_pieces[piece]}') for piece in range(len(self.player_pieces))]

        if not self.player_pieces:
            print("Status: The game is over. You won!")
            return False
        elif not self.computer_pieces:
            print("Status: The game is over. The computer won!")
            return False
        elif 1 in [1 if value == 8 else 0 for value in self.snake_bellow.values()] and self.field[0][0] == self.field[-1][1]\
                and self.snake_bellow[str(self.field[0][0])] == 8:
            print("Status: The game is over. It's a draw!")
            return False

        if self.status == 'computer':
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        elif self.status == 'player':
            print("\nStatus: It's your turn to make a move. Enter your command.")
        self.move()

    def move(self):
        while True:
            while True:
                move = input()
                if self.status == 'computer' or ((move.isdigit() or (move and move[0] == '-' and move[1::].isdigit()))
                                                 and abs(int(move)) <= len(self.player_pieces)):
                    break
                print('Invalid input. Please try again.')
            if self.status == 'computer' and not move:
                significance, check_move = dict(self.snake_bellow), len(self.computer_pieces)
                for piece in self.computer_pieces:
                    for value in piece:
                        significance[str(value)] += 1
                priority = {str(key): 0 for key in range(len(self.computer_pieces))}
                for key in range(len(self.computer_pieces)):
                    for value in self.computer_pieces[key]:
                        priority[str(key)] += significance[str(value)]
                priority = {key: value for key, value in sorted(priority.items(), key=itemgetter(1))}
                while True:
                    if not priority:
                        if self.continuation_move(self.computer_pieces, '0'):
                            self.status = 'player'
                            break
                    for step in range(2):
                        if not step:
                            move = f'-{list(priority.keys())[-1]}'
                            if self.continuation_move(self.computer_pieces, str(move)):
                                self.status = 'player'
                                break
                        else:
                            move = f'{list(priority.keys())[-1]}'
                            if self.continuation_move(self.computer_pieces, str(move)):
                                self.status = 'player'
                                break
                    del priority[f'{list(priority.keys())[-1]}']
                    if len(self.computer_pieces) != check_move:
                        break
                break
            elif self.status == 'player' and move:
                if not self.continuation_move(self.player_pieces, move):
                    print("Illegal move. Please try again.")
                else:
                    self.status = 'computer'
                    break
        if not self.show_move():
            return True

    def continuation_move(self, player, move):
        if move == '0':
            if not self.stock_pieces:
                return True
            index_piece = self.stock_pieces.index(choice(self.stock_pieces))
            player.append(self.stock_pieces[index_piece])
            del self.stock_pieces[index_piece]
            return True
        else:
            take_piece = player[abs(int(move)) - 1]
            if move[0] == '-':
                if self.field[0][0] not in take_piece:
                    return False
                elif take_piece[1] != self.field[0][0]:
                    take_piece[0], take_piece[1] = take_piece[1], take_piece[0]
            else:
                if self.field[-1][1] not in take_piece:
                    return False
                elif take_piece[0] != self.field[-1][1]:
                    take_piece[0], take_piece[1] = take_piece[1], take_piece[0]
            del player[abs(int(move)) - 1]
            self.snake_bellow[str(take_piece[0])] += 1
            self.snake_bellow[str(take_piece[1])] += 1
            if move[0] == '-':
                self.field.reverse()
                self.field.append(take_piece)
                self.field.reverse()
            else:
                self.field.append(take_piece)
            return True


if __name__ == "__main__":
    Dominoes()
