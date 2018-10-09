#!/usr/bin/env python3
import os
import time
import sys

PLAYER_1_SYMBOL = 'X'
PLAYER_2_SYMBOL = 'O'

WIN_PATTERNS = [
    [(0, 1), (0, 2), (0, 3)],
    [(1, 0), (2, 0), (3, 0)],
    [(1, -1), (2, -2), (3, -3)],
    [(1, 1), (2, 2), (3, 3)]
    ]

class Game():
    '''Game class stores game state. Init will generate game board and state.'''
    SYMBOLS = [' ', 'X', 'O']

    def __init__(self, width=7, height=6):
        self.board = [[0]*width for x in range(height)]
        self.player_1_turn = True
        self.playing = True
        self.frames = []
        self.width = width
        self.height = height

    def render_board(self):
        '''Clears terminal and renders game board to screen'''
        os.system('cls' if os.name == 'nt' else 'clear')
        print(("Welcome to connect 4. To win get 4 of your own symbols"
               " in a row in any direction. Symbols start on the top and "
               "fall down as far as they can. To play choose a column to drop your symbol.\n\n"))
        print("    "+'   '.join(['1', '2', '3', '4', '5', '6', '7'])+'  \n')
        for i in range(self.height):
            row = self.board[i]
            print("  | "+' | '.join([self.SYMBOLS[x] for x in row])+' |')
        try:
            print('  '+'█'*29+'\n')
        except UnicodeEncodeError:
            print('  '+'H'*29+'\n')

    def is_column_full(self, column):
        '''Takes an int up to 6 and returns a boolean for if that column is full'''
        return self.board[0][column] != 0

    def drop(self, column):
        '''Takes an int for the column adds frames to the class to simulate a drop returns None'''
        if self.is_column_full(column):
            raise Exception("column is full")
        depth = 1
        for i in range(self.height):
            if self.board[i][column] == 0:
                depth = i
            else:
                break
        player_int = 2
        if self.player_1_turn:
            player_int = 1
        self.frames = [[[(0, column), player_int]]]
        for f in range(1, depth+1):
            self.frames.append([[(f, column), player_int], [(f-1, column), 0]])

        self.player_1_turn = not self.player_1_turn

    def animate(self):
        '''Updates the game board according to frames. Returns False if there are no frames left'''
        if not self.frames:
            return False
        frames = self.frames.pop(0)
        for frame in frames:
            self.board[frame[0][0]][frame[0][1]] = frame[1]
        return bool(self.frames)

    def check_win(self):
        '''If won will print and change game state self.playing to False returns nothing'''
        won, pattern, start = self.check_win_patterns()
        if won:
            self.playing = False
            x_start, y_start = start
            self.board = [[0]*self.width for x_start in range(self.height)]
            self.board[y_start][x_start] = won
            for mod_y, mod_x in pattern:
                self.board[mod_y+y_start][mod_x+x_start] = won
            self.render_board()
            print(f"Game over! Player {won} has won the game!")

    def check_win_patterns(self):
        '''Takes no input. Returns (None)*3 or a
        list (winning player,winning pattern, start of pattern (x, y))'''
        for y in range(self.height):
            for x in range(self.width):
                check_player = self.board[y][x]
                if check_player == 0:
                    continue
                for pattern in WIN_PATTERNS:
                    count = 0
                    for mod_y, mod_x in pattern:
                        if x+mod_x >= self.width or x+mod_x < 0:
                            break
                        if y+mod_y >= self.height or y+mod_y < 0:
                            break
                        if self.board[mod_y+y][mod_x+x] == check_player:
                            count += 1
                        else:
                            break
                    else:
                        return check_player, pattern, (x, y)#return int, list of tuples, start
        return None, None, None

    def get_next_move(self):
        '''Prompts user for which column to drop, requires game obj'''
        p1_turn = self.player_1_turn
        if p1_turn:
            player_number = 1
            player_symbol = PLAYER_1_SYMBOL
        else:
            player_number = 2
            player_symbol = PLAYER_2_SYMBOL
        print(f'Player {player_number} choose a column to drop your {player_symbol}:', end='')
        while True:
            try:
                column = int(input())
            except ValueError:
                print(f"Please choose only a number between 1 and {self.width}")
                continue
            if column < 1 or column > self.width:
                print(f"Please choose only a number between 1 and {self.width}")
                continue
            if self.is_column_full(column-1):
                print(f"Please choose a different column. Column {column} is full")
                continue
            break
        return column-1


if __name__ == '__main__':
    game = Game()
    while game.playing:

        game.render_board()
        next_move = game.get_next_move()

        game.drop(next_move)

        while game.animate():
            time.sleep(.15)

            game.render_board()

        game.check_win()

