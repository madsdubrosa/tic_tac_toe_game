"""
Build a single-player version of tik-tac-toe, making it you vs. computer instead of 1 vs. 1
"""


from tkinter import *
import numpy as np
from random import *

GREEN = "#2F794F"


class TicTacToe:
    # ------------------------------------------------------------------
    # INITIALIZATION FUNCTIONS
    # ------------------------------------------------------------------
    def __init__(self, width=600, height=600):
        if width != height:
            width = max(width, height)
            height = max(width, height)
        self.board_size = width
        self.symbol_size = (self.board_size / 3 - self.board_size / 8) / 2
        self.symbol_thickness = 50
        self.symbol_X_color = "#000000"
        self.symbol_O_color = "#BE93D4"

        self.window = Tk()
        self.window.title("Tik-Tac-Toe")
        self.canvas = Canvas(self.window, width=width, height=height)
        self.canvas.pack()
        # input from user should be clicks:
        self.window.bind("<Button-1>", self.click)
        # initializing board state
        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros((3, 3))

        self.player_X_start = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.tie_score = 0

        self.X_wins = False
        self.X_score = 0

        self.O_wins = False
        self.O_score = 0

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * self.board_size / 3, 0, (i + 1) * self.board_size / 3, self.board_size)
            self.canvas.create_line(0, (i + 1) * self.board_size / 3, self.board_size, (i + 1) * self.board_size / 3)

    def play_game(self):
        self.window.mainloop()

    def play_again(self):
        self.initialize_board()
        self.X_wins = False
        self.O_wins = False
        self.tie = False
        self.player_X_turns = True
        self.player_X_start = True
        self.board_status = np.zeros((3, 3))

    # ------------------------------------------------------------------
    # DRAWING FUNCTIONS
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)  # grid value on the board
        grid_position = self.convert_logical_to_grid_position(logical_position)  # actual pixel values of the center of the grid
        self.canvas.create_oval(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size,
                                width=self.symbol_thickness,
                                fill=self.symbol_O_color)

    def draw_X(self, logical_position):
        logical_position = np.array(logical_position)  # grid value on the board
        grid_position = self.convert_logical_to_grid_position(logical_position)  # actual pixel values of the center of the grid
        self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size,
                                width=self.symbol_thickness,
                                fill=self.symbol_X_color)
        self.canvas.create_line(grid_position[0] + self.symbol_size, grid_position[1] - self.symbol_size,
                                grid_position[0] - self.symbol_size, grid_position[1] + self.symbol_size,
                                width=self.symbol_thickness,
                                fill=self.symbol_X_color)

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = "Winner: Player X"
            color = self.symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = "Winner: Player O"
            color = self.symbol_O_color
        else:
            self.tie_score += 1
            text = "It's a tie :("
            color = "green"

        self.canvas.delete("all")
        self.canvas.create_text(self.board_size / 2,
                                self.board_size / 3,
                                font="cmr 60 bold",
                                fill=color,
                                text=text)

        score_text = "Scores \n"
        self.canvas.create_text(self.board_size / 2,
                                5 * self.board_size / 8,
                                font="cmr 30 bold",
                                fill=color,
                                text=score_text)
        score_text = f"Player X: {self.X_score}\nPlayer O: {self.O_score}\nTie: {self.tie_score}"
        self.canvas.create_text(self.board_size / 2,
                                5 * self.board_size / 10,
                                font="cmr 20 bold",
                                fill=color,
                                text=score_text)
        self.reset_board = True
        ending_text = "Click to play again\n"
        self.canvas.create_text(self.board_size / 2,
                                5 * self.board_size / 12,
                                font="cmr 20 bold",
                                fill="black",
                                text=ending_text)

    # ------------------------------------------------------------------
    # LOGICAL FUNCTIONS
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        return (self.board_size / 3) * logical_position + self.board_size / 6

    def convert_grid_to_logical_position(self, grid_position):
        return np.array(grid_position // (self.board_size / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0], logical_position[1]] != 0

    def is_winner(self, player):
        """
        :param player: can be "X" or "O"
        :return: a boolean determining whether the player wins; True -> winner, False -> not winner
        """
        board_player = -1 if player == "X" else 1
        # row or column
        for i in range(3):
            if self.board_status[i, 0] == self.board_status[i, 1] == self.board_status[i, 2] == board_player:
                return True
            elif self.board_status[0, i] == self.board_status[1, i] == self.board_status[2, i] == board_player:
                return True

        # diagonals
        if self.board_status[0, 0] == self.board_status[1, 1] == self.board_status[2, 2] == board_player:
            return True
        elif self.board_status[0, 2] == self.board_status[1, 1] == self.board_status[2, 0] == board_player:
            return True

        return False

    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        return len(r) == 0

    def is_gameover(self):
        # either someone wins or all of the grid is occupied
        self.X_wins = self.is_winner("X")
        if not self.X_wins:
            self.O_wins = self.is_winner("O")
        if not self.X_wins and not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print("X wins")
        if self.O_wins:
            print("O wins")
        if self.tie:
            print("Tie!")

        return gameover

    def click(self, event):
        if not isinstance(event.widget, Canvas):
            return
        grid_position = np.array([event.x, event.y])
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = False
                if self.is_gameover():  # check if game is concluded
                    self.display_gameover()
                else:
                    logical_position = np.array([randint(0,2),randint(0,2)])
                    while self.is_grid_occupied(logical_position):
                        logical_position = np.array([randint(0, 2), randint(0, 2)])
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = True
                    if self.is_gameover():  # check if game is concluded
                        self.display_gameover()
        else:  # play_again()
            self.canvas.delete("all")  # this will create a fresh canvas
            self.play_again()
            self.reset_board = False


def main():
    game = TicTacToe()
    game.play_game()


main()
