import tkinter as tk
from tkinter import messagebox
import time
import winsound  # For beep sounds


class PlayerTurn:
    PLAYER1 = "Player 1"
    PLAYER2 = "Player 2"


class GameRenderer:
    def __init__(self, root, player1_name="Player 1", player2_name="Player 2"):
        self.root = root
        self.board = [[' ' for _ in range(3)] for _ in range(3)]  # Game board
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player_turn = PlayerTurn.PLAYER1
        self.player1_score = 0
        self.player2_score = 0
        self.start_time = time.time()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Button grid
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.cell_size = min(self.screen_width, self.screen_height) // 5  # Dynamically adjust cell size
        self.create_ui()

    def create_ui(self):
        """Render the game grid and options."""
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#282C34")  # Background color

        self.score_label = tk.Label(
            self.root,
            text=self.get_score_text(),
            font=('Arial', 24, 'bold'),
            bg="#282C34",
            fg="white"
        )
        self.score_label.pack(pady=10)

        self.turn_label = tk.Label(
            self.root,
            text=f"{self.player_turn}'s Turn",
            font=('Arial', 20, 'italic'),
            bg="#282C34",
            fg="cyan"
        )
        self.turn_label.pack(pady=5)

        self.timer_label = tk.Label(
            self.root,
            text=f"Time Elapsed: 0s",
            font=('Arial', 18),
            bg="#282C34",
            fg="yellow"
        )
        self.timer_label.pack(pady=5)
        self.update_timer()

        frame = tk.Frame(self.root, bg="#282C34")
        frame.pack()

        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    frame,
                    text='',
                    font=('Arial', self.cell_size // 6),
                    width=self.cell_size // 40,
                    height=self.cell_size // 100,
                    bg="#61AFEF",
                    fg="white",
                    activebackground="#98C379",
                    activeforeground="black",
                    command=lambda row=i, col=j: self.on_button_click(row, col),
                )
                button.grid(row=i, column=j, padx=10, pady=10)
                self.buttons[i][j] = button

        options_frame = tk.Frame(self.root, bg="#282C34")
        options_frame.pack(pady=20)

        self.restart_button = tk.Button(
            options_frame,
            text="Restart Game",
            font=('Arial', 16),
            bg="#E06C75",
            fg="white",
            command=self.reset_board
        )
        self.restart_button.pack(side=tk.LEFT, padx=20)

        self.exit_button = tk.Button(
            options_frame,
            text="Exit Game",
            font=('Arial', 16),
            bg="#E06C75",
            fg="white",
            command=self.root.quit
        )
        self.exit_button.pack(side=tk.LEFT, padx=20)

    def render_turn_message(self):
        """Display the current player's turn."""
        current_player = self.player1_name if self.player_turn == PlayerTurn.PLAYER1 else self.player2_name
        self.turn_label.config(text=f"{current_player}'s Turn")

    def update_button(self, row, col, symbol):
        """Update the text of the button and disable it."""
        self.buttons[row][col].config(text=symbol, state=tk.DISABLED)
        winsound.Beep(800, 100)  # Play a short beep when a button is clicked

    def reset_board(self):
        """Reset the board and the buttons."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_turn = PlayerTurn.PLAYER1
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state=tk.NORMAL, bg="#61AFEF")
        self.render_turn_message()
        self.start_time = time.time()
        self.update_timer()

    def update_score(self, winner):
        """Update the scores based on the winner."""
        if winner == 'X':
            self.player1_score += 1
        elif winner == 'O':
            self.player2_score += 1
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        """Generate the score text."""
        return f"{self.player1_name} (X): {self.player1_score}   |   {self.player2_name} (O): {self.player2_score}"

    def highlight_winner(self, winning_cells):
        """Highlight the winning cells with an animation."""
        for _ in range(5):  # Flash 5 times
            for row, col in winning_cells:
                self.buttons[row][col].config(bg="#D19A66")
            self.root.update()
            time.sleep(0.2)
            for row, col in winning_cells:
                self.buttons[row][col].config(bg="#61AFEF")
            self.root.update()
            time.sleep(0.2)

    def update_timer(self):
        """Update the game timer."""
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time Elapsed: {elapsed_time}s")
        self.root.after(1000, self.update_timer)


class GameManager:
    def __init__(self, renderer):
        self.renderer = renderer

    def on_button_click(self, row, col):
        """Handle button click events."""
        if self.renderer.board[row][col] != ' ':
            return  # Ignore if the cell is already filled

        # Update the board and UI
        symbol = 'X' if self.renderer.player_turn == PlayerTurn.PLAYER1 else 'O'
        self.renderer.board[row][col] = symbol
        self.renderer.update_button(row, col, symbol)

        # Check for a winner
        winner, winning_cells = self.check_winner()
        if winner:
            self.show_winner(winner, winning_cells)
            return

        # Switch player turns
        self.renderer.player_turn = PlayerTurn.PLAYER2 if self.renderer.player_turn == PlayerTurn.PLAYER1 else PlayerTurn.PLAYER1
        self.renderer.render_turn_message()

    def check_winner(self):
        """Check if there's a winner or a draw."""
        board = self.renderer.board

        # Check rows and columns
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return board[i][0], [(i, 0), (i, 1), (i, 2)]
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return board[0][i], [(0, i), (1, i), (2, i)]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0], [(0, 0), (1, 1), (2, 2)]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2], [(0, 2), (1, 1), (2, 0)]

        # Check for draw
        for row in board:
            if ' ' in row:
                return None, []  # Game is still ongoing
        return "Draw", []

    def show_winner(self, winner, winning_cells):
        """Show the winner or draw and reset the game."""
        if winner == "Draw":
            messagebox.showinfo("Game Over", "It's a draw!")
            winsound.Beep(500, 300)  # Different beep for draw
        else:
            winner_name = self.renderer.player1_name if winner == 'X' else self.renderer.player2_name
            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            winsound.Beep(1000, 500)  # Celebratory beep for win
            self.renderer.highlight_winner(winning_cells)
            self.renderer.update_score(winner)
        self.renderer.reset_board()


# Player Name Input and Initialization
def start_game():
    player1_name = player1_entry.get() or "Player 1"
    player2_name = player2_entry.get() or "Player 2"
    name_window.destroy()

    root = tk.Tk()
    renderer = GameRenderer(root, player1_name, player2_name)
    game_manager = GameManager(renderer)

    # Connect the renderer's button click to the game manager
    renderer.on_button_click = game_manager.on_button_click

    # Run the game loop
    root.mainloop()


# Start Game UI
name_window = tk.Tk()
name_window.title("Tic Tac Toe - Enter Player Names")

tk.Label(name_window, text="Enter Player 1 Name (X):", font=('Arial', 14)).grid(row=0, column=0, pady=5)
player1_entry = tk.Entry(name_window, font=('Arial', 14))
player1_entry.grid(row=0, column=1, pady=5)

tk.Label(name_window, text="Enter Player 2 Name (O):", font=('Arial', 14)).grid(row=1, column=0, pady=5)
player2_entry = tk.Entry(name_window, font=('Arial', 14))
player2_entry.grid(row=1, column=1, pady=5)

start_button = tk.Button(name_window, text="Start Game", font=('Arial', 16), command=start_game)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

name_window.mainloop()
