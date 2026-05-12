


from datetime import datetime, timedelta
import calendar
from transaction import create_signed_transaction
from budget_tracker import BudgetTracker
from database import (
    create_table,
    save_transaction,
    load_transactions,
    delete_transaction,
    update_transaction
)
from recurring import create_recurring_transactions

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
        notebook.add(recurring_tab, text="Recurring Transactions")
        notebook.add(weekly_tab, text="Weekly View")
        notebook.add(monthly_tab, text="Monthly View")
        

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

        self.type_var = tk.StringVar(value="expense")
        self.type_entry = ttk.Combobox(
            entry_frame,
            textvariable=self.type_var,
            values=["income", "expense"],
            state="readonly"
        )
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
            "Status",
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

        weekly_control_frame = tk.LabelFrame(
            weekly_tab,
            text="Weekly Controls",
            padx=20,
            pady=20
        )
        weekly_control_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            weekly_control_frame,
            text="Week Start Date"
        ).grid(row=0, column=0)

        self.week_var = tk.StringVar()
        self.week_dropdown = ttk.Combobox(
            weekly_control_frame,
            textvariable=self.week_var,
            values=self.get_week_options(),
            state="readonly"
        )
        self.week_dropdown.grid(row=0, column=1)

        tk.Button(
            weekly_control_frame,
            text="Load Weekly Summary",
            command=self.load_weekly_summary
        ).grid(row=0, column=2, padx=10)

        self.weekly_summary_label = tk.Label(
            weekly_tab,
            text="Select a week to view summary.",
            justify="left",
            anchor="w"
        )
        self.weekly_summary_label.pack(fill="x", padx=20, pady=10)

        weekly_category_frame = tk.LabelFrame(
            weekly_tab,
            text="Category Summary",
            padx=20,
            pady=20
        )
        weekly_category_frame.pack(fill="x", padx=20, pady=10)

        self.weekly_category_label = tk.Label(
            weekly_category_frame,
            text="Weekly category summary will appear here.",
            justify="left",
            anchor="w"
        )
        self.weekly_category_label.pack(anchor="w")

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

        weekly_columns = (
            "ID",
            "Type",
            "Amount",
            "Category",
            "Date"
        )

        self.weekly_table = ttk.Treeview(
            weekly_transactions_frame,
            columns=weekly_columns,
            show="headings"
        )

        for col in weekly_columns:
            self.weekly_table.heading(col, text=col)
            self.weekly_table.column(col, width=140)

        self.weekly_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        weekly_scrollbar = ttk.Scrollbar(
            weekly_transactions_frame,
            orient="vertical",
            command=self.weekly_table.yview
        )
        weekly_scrollbar.pack(side="right", fill="y")

        self.weekly_table.configure(
            yscrollcommand=weekly_scrollbar.set
        )



        # Monthly View Tab

        monthly_title = tk.Label(
            monthly_tab,
            text="Monthly Budget View",
            font=("Arial", 18, "bold")
        )
        monthly_title.pack(pady=10)

        monthly_control_frame = tk.LabelFrame(
            monthly_tab,
            text="Monthly Controls",
            padx=20,
            pady=20
        )
        monthly_control_frame.pack(fill="x", padx=20, pady=10)

        current_year = datetime.today().year

        tk.Label(monthly_control_frame, text="Year").grid(
            row=0,
            column=0
        )

        self.year_var = tk.StringVar(value=str(current_year))
        self.year_dropdown = ttk.Combobox(
            monthly_control_frame,
            textvariable=self.year_var,
            values=[
                str(current_year - 1),
                str(current_year),
                str(current_year + 1)
            ],
            state="readonly"
        )
        self.year_dropdown.grid(row=0, column=1)

        tk.Label(monthly_control_frame, text="Month").grid(
            row=0,
            column=2
        )

        self.month_var = tk.StringVar(value=str(datetime.today().month))
        self.month_dropdown = ttk.Combobox(
            monthly_control_frame,
            textvariable=self.month_var,
            values=[str(i) for i in range(1, 13)],
            state="readonly"
        )
        self.month_dropdown.grid(row=0, column=3)

        tk.Button(
            monthly_control_frame,
            text="Load Monthly Summary",
            command=self.load_monthly_summary
        ).grid(row=0, column=4, padx=10)

        self.monthly_summary_label = tk.Label(
            monthly_tab,
            text="Select a month to view summary.",
            justify="left",
            anchor="w"
        )
        self.monthly_summary_label.pack(fill="x", padx=20, pady=10)

        monthly_category_frame = tk.LabelFrame(
            monthly_tab,
            text="Category Summary",
            padx=20,
            pady=20
        )
        monthly_category_frame.pack(fill="x", padx=20, pady=10)

        self.monthly_category_label = tk.Label(
            monthly_category_frame,
            text="Monthly category summary will appear here.",
            justify="left",
            anchor="w"
        )
        self.monthly_category_label.pack(anchor="w")

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

        monthly_columns = (
            "ID",
            "Type",
            "Amount",
            "Category",
            "Date"
        )

        self.monthly_table = ttk.Treeview(
            monthly_transactions_frame,
            columns=monthly_columns,
            show="headings"
        )

        for col in monthly_columns:
            self.monthly_table.heading(col, text=col)
            self.monthly_table.column(col, width=140)

        self.monthly_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        monthly_scrollbar = ttk.Scrollbar(
            monthly_transactions_frame,
            orient="vertical",
            command=self.monthly_table.yview
        )
        monthly_scrollbar.pack(side="right", fill="y")

        self.monthly_table.configure(
            yscrollcommand=monthly_scrollbar.set
        )



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

        self.recurring_type_var = tk.StringVar(value="expense")
        self.recurring_type_entry = ttk.Combobox(
            recurring_frame,
            textvariable=self.recurring_type_var,
            values=["income", "expense"],
            state="readonly"
        )
        self.recurring_type_entry.grid(row=0, column=1)

        tk.Label(recurring_frame, text="Amount").grid(row=1, column=0)
        self.recurring_amount_entry = tk.Entry(recurring_frame)
        self.recurring_amount_entry.grid(row=1, column=1)

        tk.Label(recurring_frame, text="Category").grid(row=2, column=0)
        self.recurring_category_entry = tk.Entry(recurring_frame)
        self.recurring_category_entry.grid(row=2, column=1)

        tk.Label(
            recurring_frame,
            text="Start Date (YYYY-MM-DD)"
        ).grid(row=3, column=0)

        self.recurring_date_entry = tk.Entry(recurring_frame)
        self.recurring_date_entry.grid(row=3, column=1)

        tk.Label(
            recurring_frame,
            text="Frequency"
        ).grid(row=4, column=0)

        self.frequency_var = tk.StringVar(value="monthly")
        self.frequency_entry = ttk.Combobox(
            recurring_frame,
            textvariable=self.frequency_var,
            values=["weekly", "biweekly", "monthly"],
            state="readonly"
        )
        self.frequency_entry.grid(row=4, column=1)

        tk.Label(
            recurring_frame,
            text="Repeat Count"
        ).grid(row=5, column=0)

        self.repeats_entry = tk.Entry(recurring_frame)
        self.repeats_entry.grid(row=5, column=1)

        tk.Button(
            recurring_frame,
            text="Generate Recurring Transactions",
            command=self.generate_recurring_transactions
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
            transaction_date = datetime.strptime(transaction.date, "%Y-%m-%d").date()
            today = datetime.today().date()
            status = "FUTURE" if transaction_date > today else "CURRENT"

            self.transaction_table.insert(
                "",
                "end",
                values=(
                    transaction.transaction_id,
                    status,
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
        if hasattr(self, "week_dropdown"):
            self.week_dropdown["values"] = self.get_week_options()

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

        amount_value = values[3].replace("$", "")

        self.amount_entry.insert(0, amount_value)
        self.type_entry.insert(0, values[2])
        self.category_entry.insert(0, values[4])
        self.date_entry.insert(0, values[5])

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

    # Placeholder function used during GUI development for buttons that have not yet been connected to backend logic
    def placeholder(self):
        print("Placeholder function called")

    def get_week_options(self):
        weeks = set()

        for transaction in self.tracker.get_transactions():
            transaction_date = datetime.strptime(
                transaction.date,
                "%Y-%m-%d"
            ).date()

            week_start = (
                transaction_date
                - timedelta(days=transaction_date.weekday())
            )

            weeks.add(week_start.strftime("%Y-%m-%d"))

        return sorted(weeks)

    def get_category_summary_for_period(self, start_date, end_date):
        category_summary = {}

        for transaction in self.tracker.get_transactions():
            transaction_date = datetime.strptime(
                transaction.date,
                "%Y-%m-%d"
            ).date()

            if start_date <= transaction_date <= end_date:
                if transaction.t_type == "expense":
                    category = transaction.category.lower()

                    if category in category_summary:
                        category_summary[category] += abs(transaction.amount)
                    else:
                        category_summary[category] = abs(transaction.amount)

        return category_summary

    def get_transactions_for_period(self, start_date, end_date):
        matching_transactions = []

        for transaction in self.tracker.get_transactions():
            transaction_date = datetime.strptime(
                transaction.date,
                "%Y-%m-%d"
            ).date()

            if start_date <= transaction_date <= end_date:
                matching_transactions.append(transaction)

        return matching_transactions

    def load_weekly_summary(self):
        week_start = self.week_var.get()

        if week_start == "":
            messagebox.showwarning(
                "Missing Week",
                "Please select a week."
            )
            return

        summary = self.tracker.get_weekly_summary(week_start)

        start_date = summary["week_start"]
        end_date = summary["week_end"]

        starting_balance_date = (
            start_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        starting_balance = self.tracker.get_balance_by_date(
            starting_balance_date
        )

        category_summary = self.get_category_summary_for_period(
            start_date,
            end_date
        )

        transactions = self.get_transactions_for_period(
            start_date,
            end_date
        )

        self.weekly_summary_label.config(
            text=(
                f"Week: {summary['week_start']} to {summary['week_end']}\n"
                f"Starting Balance: ${starting_balance:.2f}\n"
                f"Total Income: ${summary['income']:.2f}\n"
                f"Total Expenses: ${summary['expenses']:.2f}\n"
                f"Net Change: ${summary['net']:.2f}\n"
                f"Ending Balance: ${summary['projected_balance']:.2f}"
            )
        )

        category_text = ""

        if category_summary:
            for category, total in category_summary.items():
                category_text += f"{category}: ${total:.2f}\n"
        else:
            category_text = "No expense categories for this week."

        self.weekly_category_label.config(text=category_text)

        for row in self.weekly_table.get_children():
            self.weekly_table.delete(row)

        for transaction in transactions:
            self.weekly_table.insert(
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

    def load_monthly_summary(self):
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please select a valid year and month."
            )
            return

        summary = self.tracker.get_monthly_summary(year, month)

        start_date = summary["month_start"]
        end_date = summary["month_end"]

        starting_balance_date = (
            start_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        starting_balance = self.tracker.get_balance_by_date(
            starting_balance_date
        )

        category_summary = self.get_category_summary_for_period(
            start_date,
            end_date
        )

        transactions = self.get_transactions_for_period(
            start_date,
            end_date
        )

        self.monthly_summary_label.config(
            text=(
                f"Month: {summary['month_start']} to {summary['month_end']}\n"
                f"Starting Balance: ${starting_balance:.2f}\n"
                f"Total Income: ${summary['income']:.2f}\n"
                f"Total Expenses: ${summary['expenses']:.2f}\n"
                f"Net Change: ${summary['net']:.2f}\n"
                f"Ending Balance: ${summary['projected_balance']:.2f}"
            )
        )

        category_text = ""

        if category_summary:
            for category, total in category_summary.items():
                category_text += f"{category}: ${total:.2f}\n"
        else:
            category_text = "No expense categories for this month."

        self.monthly_category_label.config(text=category_text)

        for row in self.monthly_table.get_children():
            self.monthly_table.delete(row)

        for transaction in transactions:
            self.monthly_table.insert(
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

    def generate_recurring_transactions(self):
        try:
            amount = float(self.recurring_amount_entry.get())
            t_type = self.recurring_type_entry.get().lower()
            category = self.recurring_category_entry.get()
            start_date = self.recurring_date_entry.get()
            frequency = self.frequency_entry.get().lower()
            repeats = int(self.repeats_entry.get())

            if category == "":
                messagebox.showerror(
                    "Error",
                    "Category cannot be empty."
                )
                return

            datetime.strptime(start_date, "%Y-%m-%d")

            if repeats <= 0:
                messagebox.showerror(
                    "Error",
                    "Repeats must be greater than 0."
                )
                return

            max_repeats = {
                "weekly": 52,
                "biweekly": 26,
                "monthly": 12
            }

            if repeats > max_repeats[frequency]:
                messagebox.showerror(
                    "Error",
                    f"Maximum repeats for {frequency} is "
                    f"{max_repeats[frequency]}."
                )
                return

            transactions = create_recurring_transactions(
                amount,
                t_type,
                category,
                start_date,
                frequency,
                repeats
            )

            for transaction in transactions:
                save_transaction(transaction)

            self.refresh_transactions()

            self.week_dropdown["values"] = self.get_week_options()

            messagebox.showinfo(
                "Success",
                f"{len(transactions)} recurring transactions created."
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please check amount, date, and repeat count."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()