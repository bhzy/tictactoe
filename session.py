from datetime import datetime
from game import Game
from config import LOG_PATH


class Session:
    def __init__(self, log_path=LOG_PATH):
        self.log_path = log_path
        self.datetime = datetime.now().strftime('%d.%m.%y %H:%M')

    def play(self, player1, player2, rematch=False):
        self.upd_time()
        game = Game(player1, player2)
        if rematch:
            print(f'Current score: {player1.name} {player1.score} - {player2.score} {player2.name}')
            print('Type q to quit the game.')
            print('|1|2|3|\n|4|5|6|\n|7|8|9|')
        else:
            print('First player plays with x, second with o')
            print('You will denote your move by a number as follows:')
            print('|1|2|3|\n|4|5|6|\n|7|8|9|')
            print("Type 'q' to quit the game.")
        while game.status == 'playing':
            if game.moves % 2 == 0:
                move = input(f'Waiting for {player1.name} to move:\n')
            else:
                move = input(f'Waiting for {player2.name} to move:\n')
            if move == 'q':
                game.status = 'quit'
                return
            if move not in [str(i) for i in range(1, 10)]:
                print('Use a number from 1 to 9')
                continue
            if game.state[int(move) - 1] > 0:
                print('Position occupied')
                continue
            game.move(int(move))
            game.update_grid()
            print(game.grid)
        game.print_status()
        if game.status == 'x':
            player1.up_score()
        elif game.status == 'o':
            player2.up_score()
        replay = input('Type "r" if you want to replay. Type anything else if you do not.\n')
        if replay == 'r':
            self.play(player1, player2, rematch=True)
        else:
            if game.status in ['x', 'o', 'tie']:
                self.record_log(game)

    def upd_time(self):
        self.datetime = datetime.now().strftime('%d.%m.%y %H:%M')

    def record_log(self, game):
        log_file = open(self.log_path, 'a')
        if game.player1.score + game.player2.score > 1:
            result = f'{game.player1.name} {game.player1.score} : {game.player2.score} {game.player2.name}'
        else:
            if game.status == 'x':
                result = f'{game.player1.name} won against {game.player2.name}'
            elif game.status == 'o':
                result = f'{game.player2.name} won against {game.player1.name}'
            else:
                result = f'Tie between {game.player1.name} and {game.player2.name}'
        log_string = f'{self.datetime} - {result}\n'
        log_file.write(log_string)
        log_file.close()

    def open_log(self):
        with open(self.log_path, 'r') as log_file:
            print(log_file.read())
        if input('Enter anything to get back to the menu'):
            log_file.close()

    def clear_log(self):
        with open(self.log_path, 'w'):
            pass
        print('Log cleared.')

