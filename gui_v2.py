# gui_v2.py is an expansion of gui_v1.py,
# not a rewrite. Left gui_v1.py intact for reference and backup.

# The Transactions tab below is already fully connected to:
# - SQLite database storage
# - BudgetTracker backend logic
# - Add/Edit/Delete transaction functionality
# - Transaction refresh logic
# - Current balance + category summaries
# Existing working logic was migrated directly from gui_v1.py.


# Additional backend features were added to main_v2.py after gui_v1.py
# and still need GUI hookup in the new tabs.

# New backend logic already exists in:
# - budget_tracker.py
# - recurring.py

# New backend-supported features:
# - Future-dated transaction support
# - Date-based balance handling
# - Weekly summaries
# - Monthly summaries
# - Recurring transaction generation

# Future transactions are automatically excluded from
# current balance calculations based on transaction date.

# Current balance logic already exists in:
# - is_current_transaction()
# - inside budget_tracker.py


# Weekly View tab still needs hookup to:
# get_weekly_summary()

# Monthly View tab still needs hookup to:
# get_monthly_summary()

# Recurring Transactions tab still needs hookup to:
# create_recurring_transactions()


# Continue importing backend logic directly from:
# - transaction.py
# - budget_tracker.py
# - database.py
# - recurring.py
#
# As before, do not import functionality from main_v2.py.
# main_v2.py should remain the console/testing version
# of the application. 



from transaction import create_signed_transaction
from budget_tracker import BudgetTracker
from database import (
    create_table,
    save_transaction,
    load_transactions,
    delete_transaction,
    update_transaction
)

import tkinter as tk
from tkinter import ttk, messagebox


class BudgetTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("1400x900")

        self.tracker = BudgetTracker()

        create_table()

        transactions = load_transactions()
        self.tracker.load_transactions(transactions)

        self.build_gui()

    def build_gui(self):

        # Main notebook tabs

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        transactions_tab = tk.Frame(notebook)
        weekly_tab = tk.Frame(notebook)
        monthly_tab = tk.Frame(notebook)
        recurring_tab = tk.Frame(notebook)

        notebook.add(transactions_tab, text="Transactions")
        notebook.add(weekly_tab, text="Weekly View")
        notebook.add(monthly_tab, text="Monthly View")
        notebook.add(recurring_tab, text="Recurring Transactions")



        # Transactions Tab

        title_label = tk.Label(
            transactions_tab,
            text="Budget Tracker Application",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)

        # Transaction Entry

        entry_frame = tk.LabelFrame(
            transactions_tab,
            text="Add Transaction",
            padx=20,
            pady=20
        )
        entry_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(entry_frame, text="Amount").grid(row=0, column=0)

        self.amount_entry = tk.Entry(entry_frame)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(
            entry_frame,
            text="Type (income/expense)"
        ).grid(row=1, column=0)

        self.type_entry = tk.Entry(entry_frame)
        self.type_entry.grid(row=1, column=1)

        tk.Label(entry_frame, text="Category").grid(row=2, column=0)

        self.category_entry = tk.Entry(entry_frame)
        self.category_entry.grid(row=2, column=1)

        tk.Label(
            entry_frame,
            text="Date (YYYY-MM-DD)"
        ).grid(row=3, column=0)

        self.date_entry = tk.Entry(entry_frame)
        self.date_entry.grid(row=3, column=1)

        tk.Button(
            entry_frame,
            text="Add Transaction",
            command=self.add_transaction
        ).grid(row=4, column=0, pady=10)

        # Actions

        action_frame = tk.LabelFrame(
            transactions_tab,
            text="Actions",
            padx=20,
            pady=20
        )
        action_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(
            action_frame,
            text="Edit Transaction",
            command=self.load_selected_transaction
        ).pack(side="left", padx=10)

        tk.Button(
            action_frame,
            text="Save Edit",
            command=self.save_edit_transaction
        ).pack(side="left", padx=10)

        tk.Button(
            action_frame,
            text="Delete Transaction",
            command=self.delete_transaction
        ).pack(side="left", padx=10)

        tk.Button(
            action_frame,
            text="Refresh Transactions",
            command=self.refresh_transactions
        ).pack(side="left", padx=10)

        # Transaction Table

        display_frame = tk.LabelFrame(
            transactions_tab,
            text="Transaction Display",
            padx=20,
            pady=20
        )
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "ID",
            "Type",
            "Amount",
            "Category",
            "Date"
        )

        self.transaction_table = ttk.Treeview(
            display_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.transaction_table.heading(col, text=col)
            self.transaction_table.column(col, width=140)

        self.transaction_table.pack(fill="both", expand=True)

        # Summary

        summary_frame = tk.LabelFrame(
            transactions_tab,
            text="Budget Expenses Summary",
            padx=20,
            pady=20
        )
        summary_frame.pack(fill="x", padx=20, pady=10)

        self.summary_label = tk.Label(summary_frame, text="")
        self.summary_label.pack(anchor="w")



        # Weekly View Tab

        weekly_title = tk.Label(
            weekly_tab,
            text="Weekly Budget View",
            font=("Arial", 18, "bold")
        )
        weekly_title.pack(pady=10)

        # Weekly Controls

        weekly_control_frame = tk.LabelFrame(
            weekly_tab,
            text="Weekly Controls",
            padx=20,
            pady=20
        )
        weekly_control_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            weekly_control_frame,
            text="Week Start Date (YYYY-MM-DD)"
        ).grid(row=0, column=0)

        tk.Entry(weekly_control_frame).grid(row=0, column=1)

        tk.Button(
            weekly_control_frame,
            text="Load Weekly Summary",
            command=self.placeholder  # Replace with weekly summary backend logic
        ).grid(row=0, column=2, padx=10)

        # Weekly Financial Summary

        weekly_summary_frame = tk.LabelFrame(
            weekly_tab,
            text="Weekly Financial Summary",
            padx=20,
            pady=20
        )
        weekly_summary_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            weekly_summary_frame,
            text="Starting Balance:"
        ).pack(anchor="w")

        tk.Label(
            weekly_summary_frame,
            text="Total Income:"
        ).pack(anchor="w")

        tk.Label(
            weekly_summary_frame,
            text="Total Expenses:"
        ).pack(anchor="w")

        tk.Label(
            weekly_summary_frame,
            text="Net Change:"
        ).pack(anchor="w")

        tk.Label(
            weekly_summary_frame,
            text="Ending Balance:"
        ).pack(anchor="w")

        # Weekly Category Summary

        weekly_category_frame = tk.LabelFrame(
            weekly_tab,
            text="Category Summary",
            padx=20,
            pady=20
        )
        weekly_category_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            weekly_category_frame,
            text="Weekly category summary will appear here"
        ).pack(anchor="w")

        # Weekly Transactions Table

        weekly_transactions_frame = tk.LabelFrame(
            weekly_tab,
            text="Weekly Transactions",
            padx=20,
            pady=20
        )
        weekly_transactions_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        weekly_table = ttk.Treeview(
            weekly_transactions_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            weekly_table.heading(col, text=col)
            weekly_table.column(col, width=140)

        weekly_table.pack(fill="both", expand=True)



        # Monthly View Tab

        monthly_title = tk.Label(
            monthly_tab,
            text="Monthly Budget View",
            font=("Arial", 18, "bold")
        )
        monthly_title.pack(pady=10)

        # Monthly Controls

        monthly_control_frame = tk.LabelFrame(
            monthly_tab,
            text="Monthly Controls",
            padx=20,
            pady=20
        )
        monthly_control_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(monthly_control_frame, text="Year").grid(
            row=0,
            column=0
        )

        tk.Entry(monthly_control_frame).grid(
            row=0,
            column=1
        )

        tk.Label(monthly_control_frame, text="Month").grid(
            row=0,
            column=2
        )

        tk.Entry(monthly_control_frame).grid(
            row=0,
            column=3
        )

        tk.Button(
            monthly_control_frame,
            text="Load Monthly Summary",
            command=self.placeholder  # Replace with monthly summary backend logic
        ).grid(row=0, column=4, padx=10)

        # Monthly Financial Summary

        monthly_summary_frame = tk.LabelFrame(
            monthly_tab,
            text="Monthly Financial Summary",
            padx=20,
            pady=20
        )
        monthly_summary_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            monthly_summary_frame,
            text="Starting Balance:"
        ).pack(anchor="w")

        tk.Label(
            monthly_summary_frame,
            text="Total Income:"
        ).pack(anchor="w")

        tk.Label(
            monthly_summary_frame,
            text="Total Expenses:"
        ).pack(anchor="w")

        tk.Label(
            monthly_summary_frame,
            text="Net Change:"
        ).pack(anchor="w")

        tk.Label(
            monthly_summary_frame,
            text="Ending Balance:"
        ).pack(anchor="w")

        # Monthly Category Summary

        monthly_category_frame = tk.LabelFrame(
            monthly_tab,
            text="Category Summary",
            padx=20,
            pady=20
        )
        monthly_category_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            monthly_category_frame,
            text="Monthly category summary will appear here"
        ).pack(anchor="w")

        # Monthly Transactions Table

        monthly_transactions_frame = tk.LabelFrame(
            monthly_tab,
            text="Monthly Transactions",
            padx=20,
            pady=20
        )
        monthly_transactions_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        monthly_table = ttk.Treeview(
            monthly_transactions_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            monthly_table.heading(col, text=col)
            monthly_table.column(col, width=140)

        monthly_table.pack(fill="both", expand=True)



        # Recurring Transactions Tab

        recurring_title = tk.Label(
            recurring_tab,
            text="Recurring Transactions",
            font=("Arial", 18, "bold")
        )
        recurring_title.pack(pady=10)

        recurring_frame = tk.LabelFrame(
            recurring_tab,
            text="Create Recurring Transaction",
            padx=20,
            pady=20
        )
        recurring_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(recurring_frame, text="Type").grid(row=0, column=0)
        tk.Entry(recurring_frame).grid(row=0, column=1)

        tk.Label(recurring_frame, text="Amount").grid(row=1, column=0)
        tk.Entry(recurring_frame).grid(row=1, column=1)

        tk.Label(recurring_frame, text="Category").grid(row=2, column=0)
        tk.Entry(recurring_frame).grid(row=2, column=1)

        tk.Label(
            recurring_frame,
            text="Start Date (YYYY-MM-DD)"
        ).grid(row=3, column=0)

        tk.Entry(recurring_frame).grid(row=3, column=1)

        tk.Label(
            recurring_frame,
            text="Frequency"
        ).grid(row=4, column=0)

        tk.Entry(recurring_frame).grid(row=4, column=1)

        tk.Label(
            recurring_frame,
            text="Repeat Count"
        ).grid(row=5, column=0)

        tk.Entry(recurring_frame).grid(row=5, column=1)

        tk.Button(
            recurring_frame,
            text="Generate Recurring Transactions",
            command=self.placeholder  # Replace with recurring transaction backend logic
        ).grid(row=6, column=0, pady=10)

        self.refresh_transactions()



    # Existing gui_v1 backend-connected functionality

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())

            t_type = self.type_entry.get().lower()

            if t_type not in ["income", "expense"]:
                messagebox.showerror(
                    "Error",
                    "Type must be 'income' or 'expense'"
                )
                return

            category = self.category_entry.get()
            date = self.date_entry.get()

            transaction = create_signed_transaction(
                amount,
                t_type,
                category,
                date
            )

            save_transaction(transaction)

            self.tracker.add_transaction(transaction)

            messagebox.showinfo(
                "Success",
                "Transaction added!"
            )

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

        category_summary = (
            self.tracker.get_category_summary()
        )

        summary_text = f"Current Balance: ${balance:.2f}\n"

        if category_summary:

            summary_text += "\nCategory Summary:\n"

            for category, total in category_summary.items():
                summary_text += (
                    f"{category}: ${total:.2f}\n"
                )

        self.summary_label.config(text=summary_text)

    def delete_transaction(self):

        selected_item = self.transaction_table.selection()

        if not selected_item:
            messagebox.showwarning(
                "No Selection",
                "Please select a transaction to delete."
            )
            return

        values = self.transaction_table.item(
            selected_item,
            "values"
        )

        transaction_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if confirm:

            delete_transaction(transaction_id)

            self.refresh_transactions()

            messagebox.showinfo(
                "Deleted",
                "Transaction deleted successfully."
            )

    def load_selected_transaction(self):

        selected_item = self.transaction_table.selection()

        if not selected_item:
            messagebox.showwarning(
                "No Selection",
                "Please select a transaction to edit."
            )
            return

        values = self.transaction_table.item(
            selected_item,
            "values"
        )

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

        messagebox.showinfo(
            "Edit Mode",
            "Transaction loaded. Make changes, then click Save Edit."
        )

    def save_edit_transaction(self):

        try:

            if not hasattr(
                self,
                "editing_transaction_id"
            ):
                messagebox.showwarning(
                    "No Transaction",
                    "Please select a transaction to edit first."
                )
                return

            amount = float(self.amount_entry.get())

            t_type = self.type_entry.get().lower()

            if t_type not in ["income", "expense"]:
                messagebox.showerror(
                    "Error",
                    "Type must be 'income' or 'expense'"
                )
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

            messagebox.showinfo(
                "Success",
                "Transaction updated successfully!"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Placeholder function

    def placeholder(self):
        print("Placeholder function called")


def main():
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()