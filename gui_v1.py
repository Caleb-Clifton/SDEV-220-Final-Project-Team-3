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

from transaction import create_signed_transaction
from budget_tracker import BudgetTracker
from database import create_table, save_transaction, load_transactions, delete_transaction, update_transaction

import tkinter as tk
from tkinter import ttk, messagebox

class BudgetTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("900x600")
        self.tracker = BudgetTracker()
        create_table()

        transactions = load_transactions()
        self.tracker.load_transactions(transactions)
        self.build_gui()

    def build_gui(self):
        # App Title
        title_label = tk.Label(self.root, text="Budget Tracker Application", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Placeholder for transaction entry
        entry_frame = tk.LabelFrame(self.root, text="Add Transaction", padx=20, pady=20)
        entry_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(entry_frame, text="Amount").grid(row=0, column=0)
        self.amount_entry = tk.Entry(entry_frame)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(entry_frame, text="Type (income/expense)").grid(row=1, column=0)
        self.type_entry = tk.Entry(entry_frame)
        self.type_entry.grid(row=1, column=1)

        tk.Label(entry_frame, text="Category").grid(row=2, column=0)
        self.category_entry = tk.Entry(entry_frame)
        self.category_entry.grid(row=2, column=1)

        tk.Label(entry_frame, text="Date").grid(row=3, column=0)
        self.date_entry = tk.Entry(entry_frame)
        self.date_entry.grid(row=3, column=1)

        # Placeholder for action buttons
        button_frame = tk.LabelFrame(self.root, text="Actions", padx=20, pady=20)
        button_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(button_frame, text="Add Transaction", command=self.add_transaction).pack(side="left", padx=10)
        tk.Button(button_frame, text="Edit Transaction", command=self.load_selected_transaction).pack(side="left", padx=10)
        tk.Button(button_frame, text="Save Edit", command=self.save_edit_transaction).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Transaction", command=self.delete_transaction).pack(side="left", padx=10)
        tk.Button(button_frame, text="Refresh Data", command=self.refresh_transactions).pack(side="left", padx=10)

        # Placeholder section for transaction display
        display_frame = tk.LabelFrame(self.root, text="Transaction Display", padx=20, pady=20)
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Type", "Amount", "Category", "Date")
        self.transaction_table = ttk.Treeview(display_frame, columns=columns, show="headings")

        for col in columns:
          self.transaction_table.heading(col, text=col)
          self.transaction_table.column(col, width=120)
        self.transaction_table.pack(fill="both", expand=True)

        # summary sections
        summary_frame = tk.LabelFrame(self.root, text="Budget Summary", padx=20, pady=20)
        summary_frame.pack(fill="x", expand=True, padx=20, pady=10)
        self.summary_label = tk.Label(summary_frame, text="")
        self.summary_label.pack()
        self.refresh_transactions()


    # transaction methods
    def add_transaction(self):
        try:
           amount = float(self.amount_entry.get())
           t_type = self.type_entry.get().lower()
           if t_type not in ["income", "expense"]:
             messagebox.showerror("Error", "Type must be 'income' or 'expense'")
             return
           category = self.category_entry.get()
           date = self.date_entry.get()

           transaction = create_signed_transaction(amount, t_type, category, date)

           save_transaction(transaction)
           self.tracker.add_transaction(transaction)

           messagebox.showinfo("Success", "Transaction added!")
           self.refresh_transactions()
        except Exception as e:
           messagebox.showerror("Error", str(e))
    
    def refresh_transactions(self):
        for row in self.transaction_table.get_children():
         self.transaction_table.delete(row)
        transactions = load_transactions()
        self.tracker.load_transactions(transactions)

        for transaction in transactions:
         self.transaction_table.insert(
            "",
            "end",
            values=(
                transaction.transaction_id,
                transaction.t_type,
                f"${transaction.amount:.2f}",
                transaction.category,
                transaction.date
            )
        )
         
        balance = self.tracker.get_balance()
        category_summary = self.tracker.get_category_summary()
        summary_text = f"Balance: ${balance:.2f}\n"

        if category_summary:
           summary_text += "\nCategory Summary:\n"
           for category, total in category_summary.items():
             summary_text += f"{category}: ${total:.2f}\n"
        self.summary_label.config(text=summary_text)
         
    def delete_transaction(self):
        selected_item = self.transaction_table.selection()
        if not selected_item:
         messagebox.showwarning("No Selection", "Please select a transaction to delete.")
         return

        values = self.transaction_table.item(selected_item, "values")
        transaction_id = values[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")
        if confirm:
          delete_transaction(transaction_id)
          self.refresh_transactions()
          messagebox.showinfo("Deleted", "Transaction deleted successfully.")

    def load_selected_transaction(self):
         selected_item = self.transaction_table.selection()
         if not selected_item:
          messagebox.showwarning("No Selection", "Please select a transaction to edit.")
          return

         values = self.transaction_table.item(selected_item, "values")
         self.editing_transaction_id = values[0]
         self.amount_entry.delete(0, tk.END)
         self.type_entry.delete(0, tk.END)
         self.category_entry.delete(0, tk.END)
         self.date_entry.delete(0, tk.END)

         amount_value = values[2].replace("$", "")

         self.amount_entry.insert(0, amount_value)
         self.type_entry.insert(0, values[1])
         self.category_entry.insert(0, values[3])
         self.date_entry.insert(0, values[4])

         messagebox.showinfo("Edit Mode", "Transaction loaded. Make changes, then click Save Edit.")

    def save_edit_transaction(self):
         try:
          if not hasattr(self, "editing_transaction_id"):
            messagebox.showwarning("No Transaction", "Please select a transaction to edit first.")
            return

          amount = float(self.amount_entry.get())
          t_type = self.type_entry.get().lower()

          if t_type not in ["income", "expense"]:
            messagebox.showerror("Error", "Type must be 'income' or 'expense'")
            return

          category = self.category_entry.get()
          date = self.date_entry.get()
          transaction = create_signed_transaction(
            amount,
            t_type,
            category,
            date,
            self.editing_transaction_id
        )
          update_transaction(transaction)
 
          self.refresh_transactions()

          self.amount_entry.delete(0, tk.END)
          self.type_entry.delete(0, tk.END)
          self.category_entry.delete(0, tk.END)
          self.date_entry.delete(0, tk.END)

          del self.editing_transaction_id

          messagebox.showinfo("Success", "Transaction updated successfully!")

         except Exception as e:
           messagebox.showerror("Error", str(e))
    
def main():
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()