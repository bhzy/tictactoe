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
        player_id = self.moves % 2
        self.state[n - 1] = 1 - 2 * player_id
        self.moves += 1
        if self.moves >= 5:
            self.status = self.get_status()
        self.update_grid()

    def update_grid(self):
        grid = '|1|2|3|\n|4|5|6|\n|7|8|9|'
        new_grid = ''
        count = 0
        for space in grid:
            if space in [str(i) for i in range(1, 10)]:
                if self.state[count] == 1:
                    mark = 'x'
                elif self.state[count] == -1:
                    mark = 'o'
                else:
                    mark = space
                new_grid += mark
                count += 1
            else:
                new_grid += space
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