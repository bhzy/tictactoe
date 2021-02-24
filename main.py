from datetime import datetime

LOG_PATH = 'game_log.txt'


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def up_score(self):
        self.score += 1


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.grid = '|1|2|3|\n|4|5|6|\n|7|8|9|'
        self.state = [0 for i in range(9)]
        self.moves = 0
        self.status = 'playing'

    def get_status(self):
        state = self.state
        for i in range(3):
            col = sum(state[i::3])
            row = sum(state[3 * i:3 * (i + 1)])
            if col == 3 or row == 3:
                return 'x'
            elif col == -3 or row == -3:
                return 'o'
        main_diag = sum(state[::4])
        off_diag = sum(state[2:-1:2])
        if main_diag == 3 or off_diag == 3:
            return 'x'
        elif main_diag == -3 or off_diag == -3:
            return 'o'
        if self.moves == 9:
            return 'tie'
        return 'playing'

    def move(self, n):
        p = self.moves % 2
        self.state[n - 1] = 1 - 2 * p
        self.moves += 1
        if self.moves >= 5:
            self.status = self.get_status()
        self.update_grid()

    def update_grid(self):
        grid = '|1|2|3|\n|4|5|6|\n|7|8|9|'
        new_grid = ''
        count = 0
        for c in grid:
            if c in [str(i) for i in range(1, 10)]:
                if self.state[count] == 1:
                    new_c = 'x'
                elif self.state[count] == -1:
                    new_c = 'o'
                else:
                    new_c = c
                new_grid += new_c
                count += 1
            else:
                new_grid += c
        self.grid = new_grid

    def print_status(self):
        if self.status == 'x':
            print(f'{self.player1.name} victory!')
        elif self.status == 'o':
            print(f'{self.player2.name} victory!')
        elif self.status == 'tie':
            print('Tie!')
        elif self.status == 'playing':
            print('Still playing.')


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
                n = input(f'Waiting for {player1.name} to move:\n')
            else:
                n = input(f'Waiting for {player2.name} to move:\n')
            if n == 'q':
                game.status = 'quit'
                return None
            if n not in [str(i) for i in range(1, 10)]:
                print('Use a number from 1 to 9')
                continue
            if game.state[int(n) - 1] > 0:
                print('Position occupied')
                continue
            game.move(int(n))
            game.update_grid()
            print(game.grid)
        game.print_status()
        if game.status == 'x':
            player1.up_score()
        elif game.status == 'o':
            player2.up_score()
        replay = input("Type 'r' if you want to replay. Type anything else if you don't.\n")
        if replay == 'r':
            self.play(player1, player2, rematch=True)
        else:
            if game.status in ['x', 'o', 'tie']:
                self.record_log(game)

    def upd_time(self):
        self.datetime = datetime.now().strftime('%d.%m.%y %H:%M')

    def record_log(self, game, rematch=False):
        f = open(self.log_path, 'a')
        if game.player1.score + game.player2.score > 1:
            result = f'{game.player1.name} {game.player1.score} : {game.player2.score} {game.player2.name}'
        else:
            if game.status == 'x':
                result = f'{game.player1.name} won against {game.player2.name}'
            elif game.status == 'o':
                result = f'{game.player2.name} won against {game.player1.name}'
            else:
                result = f'Tie between {game.player1.name} and {game.player2.name}'
        log_string = self.datetime + ' - ' + result + '\n'
        f.write(log_string)
        f.close()

    def open_log(self):
        with open(self.log_path, 'r') as f:
            print(f.read())
        n = input('Enter anything to get back to the menu')
        if n:
            f.close()

    def clear_log(self):
        with open(self.log_path, 'w'):
            pass
        print('Log cleared.')


def main():
    print('Welcome to TicTacToe.')
    print('Enter a number to navigate the menu.')
    session = Session()
    while True:
        print('Play (1)\nOpen log (2)\nClear log (3)\nQuit (4)')
        command = input()
        while command not in [str(i) for i in range(1, 5)]:
            command = input('Invalid index\n')
        if command == '1':
            player1_name = input('Enter the name of Player 1:\n')
            player2_name = input('Enter the name of Player 2:\n')
            player1 = Player(player1_name)
            player2 = Player(player2_name)
            session.play(player1, player2)
        elif command == '2':
            session.open_log()
            continue
        elif command == '3':
            session.clear_log()
            continue
        elif command == '4':
            break


if __name__ == '__main__':
    main()
