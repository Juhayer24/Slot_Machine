import tkinter as tk
from tkinter import messagebox
import random

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

# Symbol configuration
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

symbol_value = {
    "A": 10,
    "B": 7,
    "C": 5,
    "D": 3,
}

symbol_color = {
    "A": "red",
    "B": "blue",
    "C": "dark orange",
    "D": "green"
}


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        if all(column[line] == symbol for column in columns):
            win = values[symbol] * bet
            winnings += win
            winning_lines.append((line + 1, symbol, win))
    return winnings, winning_lines


class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Slot Machine Game")
        self.root.configure(bg="#f0f0f0")

        self.balance = 0
        self.setup_ui()

    def setup_ui(self):
        # Fonts
        label_font = ("Helvetica", 12, "bold")
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")
        symbol_font = ("Courier", 18, "bold")

        # Deposit
        tk.Label(self.root, text="Deposit $:", font=label_font, bg="#020202").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.deposit_entry = tk.Entry(self.root, font=entry_font, width=10)
        self.deposit_entry.grid(row=0, column=1, pady=5)
        tk.Button(self.root, text="Set Balance", font=button_font, command=self.set_balance, bg="#000000", fg="black").grid(row=0, column=2, padx=5)

        # Bet settings
        tk.Label(self.root, text="Lines (1-3):", font=label_font, bg="#020202").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.lines_entry = tk.Entry(self.root, font=entry_font, width=10)
        self.lines_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Bet/line $:", font=label_font, bg="#000000").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.bet_entry = tk.Entry(self.root, font=entry_font, width=10)
        self.bet_entry.grid(row=2, column=1, pady=5)

        tk.Button(self.root, text="SPIN", font=button_font, command=self.spin, bg="#060606", fg="black", width=12).grid(row=3, column=0, columnspan=3, pady=10)

        # Slot machine grid
        self.slot_frame = tk.Frame(self.root, bg="white", bd=2, relief="sunken")
        self.slot_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.symbol_labels = [[tk.Label(self.slot_frame, text=" ", font=symbol_font, width=4) for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.symbol_labels[r][c].grid(row=r, column=c, padx=5, pady=5)

        # Winnings display
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f0f0f0")
        self.result_label.grid(row=5, column=0, columnspan=3)

        # Balance
        self.balance_label = tk.Label(self.root, text="Balance: $0", font=("Helvetica", 14, "bold"), fg="black", bg="#f0f0f0")
        self.balance_label.grid(row=6, column=0, columnspan=3, pady=10)

    def set_balance(self):
        try:
            amount = int(self.deposit_entry.get())
            if amount <= 0:
                raise ValueError
            self.balance = amount
            self.update_balance()
            self.result_label.config(text="Balance set successfully.", fg="green")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid deposit amount.")

    def spin(self):
        try:
            lines = int(self.lines_entry.get())
            bet = int(self.bet_entry.get())

            if not (1 <= lines <= MAX_LINES):
                raise ValueError("Lines must be between 1 and 3.")
            if not (MIN_BET <= bet <= MAX_BET):
                raise ValueError(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")

            total_bet = lines * bet
            if total_bet > self.balance:
                raise ValueError("Insufficient balance for this bet.")

            self.balance -= total_bet
            slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
            self.display_slots(slots)

            winnings, win_lines = check_winnings(slots, lines, bet, symbol_value)
            self.balance += winnings
            self.update_balance()

            if winnings > 0:
                msg = f"You won ${winnings}!\n"
                for line, symbol, win in win_lines:
                    msg += f"Line {line} matched '{symbol}' → +${win}\n"
                self.result_label.config(text=msg.strip(), fg="green")
            else:
                self.result_label.config(text="No winnings this round.", fg="red")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def display_slots(self, slots):
        for r in range(ROWS):
            for c in range(COLS):
                symbol = slots[c][r]
                self.symbol_labels[r][c].config(
                    text=symbol,
                    fg=symbol_color.get(symbol, "black")
                )

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()
