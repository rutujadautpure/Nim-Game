import math
import tkinter as tk
from tkinter import messagebox

def display_piles(piles):
    """Updates the GUI to show the current state of piles with horizontal representation."""
    for i, pile_label in enumerate(pile_labels):
        # Clear the previous display
        pile_label.config(text="")
        
        # Create a visual representation of the pile horizontally
        visual_representation = ' '.join(['🟢' for _ in range(piles[i])])
        pile_label.config(text=f"Pile {i + 1}: {visual_representation}")

def is_game_over(piles):
    """Checks if the game is over (no stones left in any pile)."""
    return sum(piles) == 0

def minimax(piles, depth, is_maximizing_player, alpha, beta):
    """Minimax function with alpha-beta pruning."""
    if is_game_over(piles):
        return -1 if is_maximizing_player else 1

    if is_maximizing_player:
        max_eval = -math.inf
        for i in range(len(piles)):
            for remove in range(1, piles[i] + 1):
                new_piles = piles[:]
                new_piles[i] -= remove
                eval = minimax(new_piles, depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(len(piles)):
            for remove in range(1, piles[i] + 1):
                new_piles = piles[:]
                new_piles[i] -= remove
                eval = minimax(new_piles, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move(piles):
    """Determines the best move for the computer using minimax with alpha-beta pruning."""
    best_val = -math.inf
    best_move = None
    alpha, beta = -math.inf, math.inf

    for i in range(len(piles)):
        for remove in range(1, piles[i] + 1):
            new_piles = piles[:]
            new_piles[i] -= remove
            move_val = minimax(new_piles, 0, False, alpha, beta)
            if move_val > best_val:
                best_val = move_val
                best_move = (i, remove)

    return best_move

def player_turn():
    """Handles the player's turn based on GUI inputs."""
    try:
        pile_index = int(pile_entry.get()) - 1
        stones_to_remove = int(stones_entry.get())
        
        if piles[pile_index] <= 0:
            messagebox.showerror("Error", "That pile is empty. Try again.")
            return
        if stones_to_remove <= 0 or stones_to_remove > piles[pile_index]:
            messagebox.showerror("Error", "Invalid number of stones. Try again.")
            return
        
        piles[pile_index] -= stones_to_remove
        display_piles(piles)

        if is_game_over(piles):
            messagebox.showinfo("Game Over", "Congratulations, you won!")
            return  # Do not quit; allow for reset

        computer_turn()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for pile and stones.")
    except IndexError:
        messagebox.showerror("Error", "Invalid pile number. Try again.")

def computer_turn():
    """Handles the computer's turn using alpha-beta pruning."""
    pile_index, stones_to_remove = best_move(piles)
    piles[pile_index] -= stones_to_remove
    display_piles(piles)
    
    messagebox.showinfo("PC's Turn", f"PC removes {stones_to_remove} stones from pile {pile_index + 1}.")
    
    if is_game_over(piles):
        messagebox.showinfo("Game Over", "PC won! Better luck next time.")

def reset_game():
    """Resets the game to the initial state."""
    global piles
    piles = [1, 3, 4, 5]  # Reset piles
    display_piles(piles)
    pile_entry.delete(0, tk.END)  # Clear entry field
    stones_entry.delete(0, tk.END)  # Clear entry field

# Setup the game
# piles = [1, 3, 5]  # Initial pile configuration
piles = [1, 3, 4, 5]  # Initial pile configuration







root = tk.Tk()
root.title("Nim Game")
root.configure(bg="#f0f8ff")

# Create a frame for the game
frame = tk.Frame(root, bg="#f0f8ff", padx=20, pady=20)
frame.pack(pady=20)

# Display the piles
pile_labels = [tk.Label(frame, text="", font=("Courier", 18), bg="#f0f8ff") for _ in range(len(piles))]
for label in pile_labels:
    label.pack(pady=5)

# Entry fields for player's input
pile_label = tk.Label(frame, text="Choose a pile: ", font=("Arial", 14), bg="#f0f8ff")
pile_label.pack(pady=5)
pile_entry = tk.Entry(frame, font=("Arial", 14))
pile_entry.pack(pady=5)

stones_label = tk.Label(frame, text="Enter the number of stones to remove:", font=("Arial", 14), bg="#f0f8ff")
stones_label.pack(pady=5)
stones_entry = tk.Entry(frame, font=("Arial", 14))
stones_entry.pack(pady=5)

# Button to submit the player's turn
submit_button = tk.Button(frame, text="Submit Move", command=player_turn, font=("Arial", 14), bg="#5cb85c", fg="white", activebackground="#4cae4c")
submit_button.pack(pady=10)

# Button to reset the game
reset_button = tk.Button(frame, text="Reset Game", command=reset_game, font=("Arial", 14), bg="#d9534f", fg="white", activebackground="#c9302c")
reset_button.pack(pady=10)

# Initialize the display
display_piles(piles)
root.mainloop()
