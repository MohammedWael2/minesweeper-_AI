import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

class Mohamed_MinesweeperGame:
    def __init__(self, rows, cols, mine_numbers):
        # Initialize game parameters
        self.rows = rows
        self.cols = cols
        self.mine_numbers = mine_numbers
        self.screen_ = [[' ' for _ in range(cols)] for _ in range(rows)]  # Initialize empty game screen_
        self.mines = set()  # Set to store mine positions
        self.is_game_over = False  # Flag to track game over status
        self.hint_tries = 3  # Number of hint tries allowed

        # Create the main window
        self.window = tk.Tk()

        # Initialize 2D array to store buttons
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]

        # Create GUI widgets
        self.create_widgets()

        # Place mines on the screen_
        self.set_mines_places()

    def create_widgets(self):
        # Set window title
        self.window.title("Minesweeper")

        # Create buttons for the game screen_
        for r in range(self.rows):
            for c in range(self.cols):
                # Create button and bind click event to reveal method
                button = tk.Button(self.window, width=3, command=lambda row=r, col=c: self.reveal(row, col))
                button.grid(row=r, column=c)  # Grid layout
                self.buttons[r][c] = button  # Store button in the 2D array

        # Add Try Again button
        try_again_button = tk.Button(self.window, text="Try Again", command=self.reset_game)
        try_again_button.grid(row=self.rows, column=0, columnspan=self.cols, sticky='we')

        # Add Hint AI button
        hint_button = tk.Button(self.window, text="Hint AI", command=self.get_hint)
        hint_button.grid(row=self.rows + 1, column=0, columnspan=self.cols, sticky='we')

    def set_mines_places(self):
        # Get all possible positions
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]

        # Randomly select mine positions
        self.mines = set(random.sample(all_positions, self.mine_numbers))

    def is_valid_position(self, row, col): # has no mines  --> 0 number
        # Check if position is valid
        return 0 <= row < self.rows and 0 <= col < self.cols

    def count_adjacent_mines(self, row, col): # المجاورة
        # Count adjacent mines for a given cell
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if self.is_valid_position(new_row, new_col) and (new_row, new_col) in self.mines:
                    count += 1
        return count

    def reveal(self, row, col): # ميثود اكتشاف الازرار
        # Reveal cell contents
        if self.is_game_over: # لو تمام  ومحصلش جيم أوفر
            return

        if (row, col) in self.mines:
            self.is_game_over = True
            self.buttons[row][col].config(text='*', bg='red')  # Show mine and end game
            self.show_mines() # في حالة ظهور قنبلة
            messagebox.showinfo("Game Over", "You hit a mine! Try again my Friend.")
            return

        mine_count = self.count_adjacent_mines(row, col)
        self.screen_[row][col] = str(mine_count)  # Update screen_ with mine count
        self.buttons[row][col].config(text=str(mine_count), bg='light gray', state='disabled')  # Update button appearance

        if mine_count == 0:
            # If no adjacent mines, recursively reveal neighboring cells
            queue = deque([(row, col)])
            visited = set([(row, col)])

            while queue: # usnig BFS algorithm
                r, c = queue.popleft()
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        new_row, new_col = r + dr, c + dc
                        if self.is_valid_position(new_row, new_col) and (new_row, new_col) not in visited:
                            mine_count = self.count_adjacent_mines(new_row, new_col)
                            self.screen_[new_row][new_col] = str(mine_count)
                            self.buttons[new_row][new_col].config(text=str(mine_count), bg='light gray', state='disabled')
                            visited.add((new_row, new_col))
                            if mine_count == 0:
                                queue.append((new_row, new_col))

    def show_mines(self):
        # Show all mines on the screen_
        for (row, col) in self.mines:
            if self.screen_[row][col] != ' ':
                continue
            self.buttons[row][col].config(text='*', bg='gray', state='disabled')

    def get_hint(self):
        # Provide a hint for the next play using BFS algorithm
        if self.hint_tries > 0:
            queue = deque([(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))])
            visited = set(queue)

            while queue:
                row, col = queue.popleft()
                if self.screen_[row][col] == ' ' and (row, col) not in self.mines:
                    self.buttons[row][col].config(bg='yellow')  # Highlight hint position
                    self.hint_tries -= 1  # Decrement hint tries
                    return
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        new_row, new_col = row + dr, col + dc
                        if self.is_valid_position(new_row, new_col) and (new_row, new_col) not in visited:
                            queue.append((new_row, new_col))
                            visited.add((new_row, new_col))
        else: # عدد المحاولات انتهت
            messagebox.showinfo("No More Hints", "You've used all your hint tries.")

    def reset_game(self):
        # Reset the game
        self.window.destroy() #close window
        self.__init__(self.rows, self.cols, self.mine_numbers)

    def run(self):
        # Start the main event loop
        self.window.mainloop()

# Play the game
game = Mohamed_MinesweeperGame(8, 8, 10)  # 11x11 grid with 10 mines
game.run()
