# This file is the starting point for the Tkinter GUI version of the Budget Tracker.
# It is not connected to the backend yet.

# IMPORTANT:
# Do not import logic from main_v2.py.
# main_v2.py will serve as the console-only version of the app.
# This GUI should import functions from the shared backend files instead:
# transaction.py, budget_tracker.py, and database.py.

# Suggested backend imports when ready:
# from transaction import Transaction, create_signed_transaction
# from budget_tracker import BudgetTracker
# from database import create_table, save_transaction, load_transactions, update_transaction, delete_transaction

# Suggested GUI connection flow:
# 1. Create a BudgetTracker object when the GUI starts.
# 2. Call create_table() to make sure the SQLite table exists.
# 3. Load saved transactions from the database.
# 4. Display transactions in the GUI.
# 5. When Add/Edit/Delete buttons are clicked, update the database first.
# 6. Refresh the BudgetTracker object and GUI display after every change.

# Placeholder methods below should eventually be replaced with real logic as functions in this file that connect to the backend. For now, they just show message boxes when clicked.
# add_transaction_placeholder()
# edit_transaction_placeholder()
# delete_transaction_placeholder()
# refresh_data_placeholder()



import dis
from pydoc import text
import tkinter as tk
from tkinter import ttk, messagebox

class BudgetTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("900x600")

        self.build_gui()

    def build_gui(self):
        # App Title
        title_label = tk.Label(self.root, text="Budget Tracker Application", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Placeholder for transaction entry
        entry_frame = tk.LabelFrame(self.root, text="Add Transaction", padx=20, pady=20)
        entry_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(entry_frame, text="GUI input fields will go here").pack()

        # Placeholder for action buttons
        button_frame = tk.LabelFrame(self.root, text="Actions", padx=20, pady=20)
        button_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(button_frame, text="Add Transaction", command=self.add_transaction_placeholder).pack(side="left", padx=10)
        tk.Button(button_frame, text="Edit Transaction", command=self.edit_transaction_placeholder).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Transaction", command=self.delete_transaction_placeholder).pack(side="left", padx=10)
        tk.Button(button_frame, text="Refresh Data", command=self.refresh_data_placeholder).pack(side="left", padx=10)

        # Placeholder section for transaction display
        display_frame = tk.LabelFrame(self.root, text="Display Transactions", padx=20, pady=20)
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(display_frame, text="Transaction display will go here").pack()

        # Placeholder section for transaction display
        display_frame = tk.LabelFrame(self.root, text="Transaction Display", padx=20, pady=20)
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(display_frame, text="Transaction display will go here").pack()

        # Placeholder section for sumarries
        summary_frame = tk.LabelFrame(self.root, text="Budget Summary", padx=20, pady=20)
        summary_frame.pack(fill="x", expand=True, padx=20, pady=10)

        tk.Label(summary_frame, text="Balance / Reports / Category summary will go here").pack()


    # Placeholder methods
    def add_transaction_placeholder(self):
        messagebox.showinfo("Add Transaction", "Add transaction functionality will be implemented here.")

    def edit_transaction_placeholder(self):
        messagebox.showinfo("Edit Transaction", "Edit transaction functionality will be implemented here.")

    def delete_transaction_placeholder(self):
        messagebox.showinfo("Delete Transaction", "Delete transaction functionality will be implemented here.")

    def refresh_data_placeholder(self):
        messagebox.showinfo("Refresh Data", "Refresh data functionality will be implemented here.")

    
def main():
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()