from datetime import datetime

from session import Session
from player import Player


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
            exit()


if __name__ == '__main__':
    main()
