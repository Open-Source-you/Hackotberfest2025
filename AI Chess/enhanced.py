import tkinter as tk
from tkinter import messagebox
import chess
import chess.engine
import os
from typing import Optional, Tuple
from PIL import Image, ImageTk
import time

class ChessGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Chess Game")
        self.geometry("1000x650")

        self.board = chess.Board()
        self.engine = self.init_stockfish()
        self.player_color = None # True for White, False for Black

        self.square_size = 75
        self.board_size = 8 * self.square_size
        self.piece_images = {}
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None

        self.captured_pieces = {'w': [], 'b': []}
        self.captured_piece_images = {}

        self.player_time = 600  # 10 minutes in seconds
        self.ai_time = 600
        self.timer_running = False
        self.last_move_time = None

        self.create_widgets()
        self.load_piece_images()
        self.draw_board()
        self.draw_pieces()
        self.choose_time()
        self.choose_color()

    def choose_time(self):
        time_window = tk.Toplevel(self)
        time_window.title("Choose Time Control")
        time_window.geometry("300x200")
        time_window.transient(self)
        time_window.grab_set()

        def set_time(minutes):
            self.player_time = minutes * 60
            self.ai_time = minutes * 60
            # Update clock display after setting new time
            if hasattr(self, 'player_clock_label'):
                self.initialize_clock_display()
            time_window.destroy()

        tk.Label(time_window, text="Select Time Control:", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(time_window, text="3 Minutes", command=lambda: set_time(3)).pack(pady=5)
        tk.Button(time_window, text="5 Minutes", command=lambda: set_time(5)).pack(pady=5)
        tk.Button(time_window, text="10 Minutes", command=lambda: set_time(10)).pack(pady=5)
        tk.Button(time_window, text="20 Minutes", command=lambda: set_time(20)).pack(pady=5)
        
        self.wait_window(time_window)

    def initialize_clock_display(self):
        """Initialize the clock display with current time values"""
        player_mins, player_secs = divmod(self.player_time, 60)
        ai_mins, ai_secs = divmod(self.ai_time, 60)
        self.player_clock_label.config(text=f"Player: {player_mins:02d}:{player_secs:02d}")
        self.ai_clock_label.config(text=f"AI: {ai_mins:02d}:{ai_secs:02d}")

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=self.board_size, height=self.board_size)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<ButtonPress-1>", self.on_piece_press)
        self.canvas.bind("<B1-Motion>", self.on_piece_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_piece_release)

        self.drag_data: dict[str, Optional[int]] = {"square": None, "item": None}

        right_panel = tk.Frame(self)
        right_panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        self.white_captured_frame = tk.Frame(right_panel)
        self.white_captured_frame.pack(pady=5)
        
        self.player_clock_label = tk.Label(right_panel, text="", font=("Helvetica", 16))
        self.player_clock_label.pack(pady=5)

        self.move_history_text = tk.Text(right_panel, height=20, width=30)
        self.move_history_text.pack()

        self.ai_clock_label = tk.Label(right_panel, text="", font=("Helvetica", 16))
        self.ai_clock_label.pack(pady=5)

        self.black_captured_frame = tk.Frame(right_panel)
        self.black_captured_frame.pack(pady=5)

        self.reset_button = tk.Button(right_panel, text="New Game", command=self.reset_game)
        self.reset_button.pack(pady=10)

    def init_stockfish(self):
        possible_paths = [
            os.path.join(os.getcwd(), 'stockfish', 'stockfish.exe'),
            os.path.join(os.getcwd(), 'stockfish.exe'),
            r'C:\Program Files (x86)\Stockfish\stockfish.exe'
        ]
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    engine = chess.engine.SimpleEngine.popen_uci(path)
                    return engine
                except Exception as e:
                    print(f"Failed to load Stockfish from {path}: {str(e)}")
        print("Warning: Stockfish not found. AI moves will be disabled.")
        return None

    def load_piece_images(self):
        pieces = {}
        for color in ['w', 'b']:
            for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
                try:
                    image = Image.open(f'pieces/{color}{piece}.png')
                    image = image.resize((self.square_size - 10, self.square_size - 10), Image.Resampling.LANCZOS)
                    pieces[f'{color}{piece}'] = ImageTk.PhotoImage(image)
                except FileNotFoundError:
                    print(f"Warning: Could not load image for {color}{piece}")
        self.piece_images = pieces

    def choose_color(self):
        color_window = tk.Toplevel(self)
        color_window.title("Choose Your Color")
        color_window.geometry("300x100")
        color_window.transient(self)
        color_window.grab_set()

        def select_white():
            self.player_color = True
            color_window.destroy()
            self.start_timer()

        def select_black():
            self.player_color = False
            color_window.destroy()
            self.start_timer()
            self.after(500, self.make_ai_move)

        tk.Button(color_window, text="Play as White", command=select_white).pack(pady=10)
        tk.Button(color_window, text="Play as Black", command=select_black).pack(pady=10)
        self.wait_window(color_window)
        self.update_clock_display()


    def draw_board(self):
        self.canvas.delete("square")
        for row in range(8):
            for col in range(8):
                color = "#D1E4F0" if (row + col) % 2 == 0 else "#7B9EBB"
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for square in chess.SQUARES:
            if self.drag_data["square"] == square:
                continue
            piece = self.board.piece_at(square)
            if piece:
                piece_symbol = piece.symbol().lower()
                color = 'w' if piece.color == chess.WHITE else 'b'
                image = self.piece_images.get(f'{color}{piece_symbol}')
                if image:
                    row, col = divmod(square, 8)
                    if self.player_color: # White's perspective
                        y = (7 - row) * self.square_size
                        x = col * self.square_size
                    else: # Black's perspective
                        y = row * self.square_size
                        x = (7-col) * self.square_size

                    self.canvas.create_image(x + self.square_size // 2, y + self.square_size // 2, image=image, tags=("piece", f"sq_{square}"))

    def on_piece_press(self, event):
        if self.board.is_game_over() or (self.board.turn == chess.BLACK and self.player_color) or (self.board.turn == chess.WHITE and not self.player_color):
            return

        col = event.x // self.square_size
        row = event.y // self.square_size
        if self.player_color:
            square = chess.square(col, 7 - row)
        else:
            square = chess.square(7 - col, row)

        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:
            items = self.canvas.find_withtag(f"sq_{square}")
            if not items:
                return

            self.selected_square = square
            self.valid_moves = [move for move in self.board.legal_moves if move.from_square == square]
            
            self.drag_data["square"] = square
            self.drag_data["item"] = items[0]
            self.canvas.tag_raise(self.drag_data["item"])
            self.highlight_valid_moves()

    def on_piece_drag(self, event):
        if self.drag_data["item"]:
            self.canvas.coords(self.drag_data["item"], event.x, event.y)

    def on_piece_release(self, event):
        if not self.drag_data.get("item") or self.drag_data.get("square") is None:
            return

        self.canvas.delete("highlight")
        
        from_square = self.drag_data["square"]
        
        if from_square is None:
            return
        
        col = event.x // self.square_size
        row = event.y // self.square_size
        if self.player_color:
            to_square = chess.square(col, 7 - row)
        else:
            to_square = chess.square(7 - col, row)

        move = chess.Move(from_square, to_square)

        # Reset drag data before any potential redraw
        self.drag_data["square"] = None
        self.drag_data["item"] = None
        self.selected_square = None

        if move in self.valid_moves:
            self.make_move(move)
            if not self.board.is_game_over():
                self.after(500, self.make_ai_move)
        else:
            # Invalid move, snap piece back by redrawing
            self.draw_pieces()

        self.valid_moves = []

    def highlight_valid_moves(self):
        for move in self.valid_moves:
            row, col = divmod(move.to_square, 8)
            if self.player_color:
                y = (7 - row) * self.square_size
                x = col * self.square_size
            else:
                y = row * self.square_size
                x = (7-col) * self.square_size

            self.canvas.create_oval(x + self.square_size//2 - 10, y + self.square_size//2 - 10,
                                    x + self.square_size//2 + 10, y + self.square_size//2 + 10,
                                    fill="green", stipple="gray50", tags="highlight")

    def make_move(self, move):
        if not self.timer_running:
            self.start_timer()
        
        if self.board.is_capture(move):
            captured_piece = self.board.piece_at(move.to_square)
            if captured_piece:
                color = 'w' if captured_piece.color == chess.WHITE else 'b'
                self.captured_pieces[color].append(captured_piece.symbol())
                self.update_captured_pieces_display()

        turn_before_move = self.board.turn
        
        move_san = self.board.san(move)
        self.board.push(move)
        self.last_move = move
        
        # Reset timer for the next player's turn
        self.last_move_time = time.time()
        
        self.update_move_history(move_san)
        self.draw_board()
        self.draw_pieces()
        self.check_game_over()
        self.update_clock_display()

    def make_ai_move(self):
        if not self.board.is_game_over() and self.engine:
            result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
            self.make_move(result.move)

    def update_move_history(self, move_san):
        if self.board.turn == chess.BLACK: # White's move
            self.move_history_text.insert(tk.END, f"{self.board.fullmove_number}. {move_san} ")
        else: # Black's move
            self.move_history_text.insert(tk.END, f"{move_san}\n")
        self.move_history_text.see(tk.END)


    def check_game_over(self):
        if self.board.is_game_over():
            # Stop the timer when game ends
            self.stop_timer()
            
            # Change background color to indicate game over
            self.change_game_over_background()
            
            result = self.board.result()
            if self.board.is_checkmate():
                winner = "White" if result == "1-0" else "Black"
                self.show_popup(f"Checkmate! {winner} wins.")
            elif self.board.is_stalemate():
                self.show_popup("Draw by Stalemate")
            elif self.board.is_insufficient_material():
                self.show_popup("Draw by Insufficient Material")
            else:
                self.show_popup(f"Game over: {result}")
        elif self.board.is_check():
            self.show_popup("Check")

    def change_game_over_background(self):
        """Change the background color when game is over"""
        # Change main window background to a soft mint green color for excellent piece visibility
        self.configure(bg='#F0FFF0')  # Honeydew - very light mint green
        
        # Use a subtle tinted background that won't interfere with pieces
        self.canvas.configure(bg='#F5FFFA')  # Mint Cream - extremely light mint
        
        # Update all frames to match the new theme
        try:
            # Find all frame widgets and update their background
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg='#F0FFF0')  # Honeydew
                    # Update child widgets in frames
                    for child in widget.winfo_children():
                        if isinstance(child, (tk.Label, tk.Button, tk.Frame)):
                            if isinstance(child, tk.Button):
                                child.configure(bg='#98FB98', activebackground='#90EE90')  # Light green colors
                            elif isinstance(child, tk.Label):
                                child.configure(bg='#F0FFF0', fg='#006400')  # Dark green text on light background
                            elif isinstance(child, tk.Frame):
                                child.configure(bg='#F0FFF0')
        except Exception as e:
            print(f"Error updating background: {e}")

    def reset_background(self):
        """Reset background to normal colors"""
        # Reset main window background to default
        self.configure(bg='SystemButtonFace')  # Default tkinter background
        
        # Reset canvas background
        self.canvas.configure(bg='white')
        
        # Reset all frames to default
        try:
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg='SystemButtonFace')
                    for child in widget.winfo_children():
                        if isinstance(child, (tk.Label, tk.Button, tk.Frame)):
                            if isinstance(child, tk.Button):
                                child.configure(bg='SystemButtonFace', activebackground='SystemButtonFace')
                            elif isinstance(child, tk.Label):
                                child.configure(bg='SystemButtonFace', fg='black')
                            elif isinstance(child, tk.Frame):
                                child.configure(bg='SystemButtonFace')
        except Exception as e:
            print(f"Error resetting background: {e}")

    def show_popup(self, message):
        popup = tk.Toplevel(self)
        popup.wm_overrideredirect(True)
        
        # Center the popup on the board
        x = self.winfo_x() + self.canvas.winfo_x() + (self.board_size - 400) // 2
        y = self.winfo_y() + self.canvas.winfo_y() + (self.board_size - 200) // 2
        popup.geometry(f"400x200+{x}+{y}")

        # Use different colors for game-ending messages
        if any(word in message.lower() for word in ['checkmate', 'wins', 'ran out', 'draw']):
            popup.configure(bg='#FFD700', relief='solid', borderwidth=3)  # Gold background for game end
            label = tk.Label(popup, text=message, font=("Helvetica", 28, "bold"), 
                           bg='#FFD700', fg='#8B0000')  # Dark red text on gold
        else:
            popup.configure(bg='lightgrey', relief='solid', borderwidth=1)
            label = tk.Label(popup, text=message, font=("Helvetica", 32, "bold"), bg='lightgrey')
        
        label.pack(expand=True)
        
        # Keep game-ending messages longer
        duration = 4000 if any(word in message.lower() for word in ['checkmate', 'wins', 'ran out', 'draw']) else 2000
        self.after(duration, popup.destroy)

    def reset_game(self):
        self.board.reset()
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
        self.move_history_text.delete(1.0, tk.END)
        self.timer_running = False
        self.last_move_time = None
        # Reset timer values will be set by choose_time()
        self.captured_pieces = {'w': [], 'b': []}
        
        # Reset background to normal colors
        self.reset_background()
        
        self.update_captured_pieces_display()
        self.draw_board()
        self.draw_pieces()
        self.choose_time()
        self.choose_color()
        self.update_clock_display()

    def update_captured_pieces_display(self):
        for widget in self.white_captured_frame.winfo_children():
            widget.destroy()
        for widget in self.black_captured_frame.winfo_children():
            widget.destroy()

        for color, frame in [('w', self.white_captured_frame), ('b', self.black_captured_frame)]:
            for piece_symbol in self.captured_pieces[color]:
                piece_key = f"{color.lower()}{piece_symbol.lower()}"
                if piece_key not in self.captured_piece_images:
                    try:
                        image = Image.open(f'pieces/{color.lower()}{piece_symbol.lower()}.png')
                        image = image.resize((30, 30), Image.Resampling.LANCZOS)
                        self.captured_piece_images[piece_key] = ImageTk.PhotoImage(image)
                    except FileNotFoundError:
                        continue
                
                image_label = tk.Label(frame, image=self.captured_piece_images[piece_key])
                image_label.pack(side=tk.LEFT)

    def start_timer(self):
        self.timer_running = True
        self.last_move_time = time.time()
        self.update_clock_display()
        self.schedule_timer_update()

    def stop_timer(self):
        self.timer_running = False

    def schedule_timer_update(self):
        if self.timer_running:
            self.after(100, self.update_clocks)

    def update_clocks(self):
        if not self.timer_running:
            return

        current_time = time.time()
        if self.last_move_time is not None:
            time_elapsed = current_time - self.last_move_time
            
            # Determine whose turn it is and deduct time accordingly
            if ((self.board.turn == chess.WHITE and self.player_color) or 
                (self.board.turn == chess.BLACK and not self.player_color)):
                # It's the player's turn
                self.player_time -= time_elapsed
            else:
                # It's the AI's turn  
                self.ai_time -= time_elapsed
        
        self.last_move_time = current_time
        self.update_clock_display()

        # Check for time out
        if self.player_time <= 0:
            self.stop_timer()
            self.change_game_over_background()
            self.show_popup("You ran out of time! AI wins.")
            return
        if self.ai_time <= 0:
            self.stop_timer()
            self.change_game_over_background()
            self.show_popup("AI ran out of time! You win.")
            return

        # Schedule next update
        self.schedule_timer_update()

    def update_clock_display(self):
        """Update the visual display of both clocks"""
        player_mins, player_secs = divmod(max(0, int(self.player_time)), 60)
        ai_mins, ai_secs = divmod(max(0, int(self.ai_time)), 60)

        self.player_clock_label.config(text=f"Player: {player_mins:02d}:{player_secs:02d}")
        self.ai_clock_label.config(text=f"AI: {ai_mins:02d}:{ai_secs:02d}")

    def on_closing(self):
        if self.engine:
            self.engine.quit()
        self.destroy()

if __name__ == "__main__":
    app = ChessGui()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()