from datetime import date, datetime
import select
from recurring import create_recurring_transactions
from transaction import Transaction
from budget_tracker import BudgetTracker
from database import create_table, delete_transaction, save_transaction, load_transactions, delete_transaction, update_transaction

def refresh_tracker():
    saved_transactions = load_transactions()
    tracker.load_transactions(saved_transactions)

def get_positive_amount():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than 0")
            return None
        return amount
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return None


def get_required_text(prompt):
    value = input(prompt).strip()
    if value == "":
        print("This field cannot be empty.")
        return None
    return value

def get_valid_date(prompt):
    date_text = input(prompt).strip()

    if date_text == "":
        print("Date cannot be empty.")
        return None

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        print("Invalid date. Please use YYYY-MM-DD format.")
        return None


def create_transaction(t_type):
    amount = get_positive_amount()
    if amount is None:
        return None

    category = get_required_text("Enter category: ")
    if category is None:
        return None

    date = get_valid_date("Enter date (YYYY-MM-DD): ")
    if date is None:
        return None

    if t_type == "expense":
        amount = -amount
    print("DEBUG:", t_type, amount)    
    return Transaction(amount, t_type, category, date)


def create_recurring_transaction_set():
    t_type = get_required_text(
        "Enter transaction type (income/expense): "
    )

    if t_type is None:
        return None

    t_type = t_type.lower()

    if t_type not in ["income", "expense"]:
        print("Type must be income or expense.")
        return None

    amount = get_positive_amount()

    if amount is None:
        return None

    category = get_required_text("Enter category: ")

    if category is None:
        return None

    start_date = get_valid_date(
        "Enter start date (YYYY-MM-DD): "
    )

    if start_date is None:
        return None

    frequency = get_required_text(
        "Enter frequency (weekly/biweekly/monthly): "
    )

    if frequency is None:
        return None

    frequency = frequency.lower()

    if frequency not in ["weekly", "biweekly", "monthly"]:
        print("Invalid frequency.")
        return None

    max_repeats = {
        "weekly": 52,
        "biweekly": 26,
        "monthly": 12
    }

    try:
        repeats = int(input("Enter number of repeats: "))

        if repeats <= 0:
            print("Repeats must be greater than 0.")
            return None
        
        if repeats > max_repeats[frequency]:
            print(f"Repeats must be less than or equal to {max_repeats[frequency]} for {frequency} frequency.")
            return None

    except ValueError:
        print("Invalid repeat count.")
        return None

    return create_recurring_transactions(
        amount,
        t_type,
        category,
        start_date,
        frequency,
        repeats
    )


def show_menu():
    print("\n1. Add Income")
    print("2. Add Expense")
    print("3. Show Balance")
    print("4. Show Transactions")
    print("5. Exit")
    print("6. Show Category Summary")
    print("7. Delete Transaction")
    print("8. Edit Transaction")
    print("9. Weekly Summary")
    print("10. Monthly Summary")
    print("11. Add Recurring Transaction")


def run_app():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            transaction = create_transaction("income")
            if transaction:
                save_transaction(transaction)
                refresh_tracker()

        elif choice == "2":
            transaction = create_transaction("expense")
            if transaction:
                save_transaction(transaction)
                refresh_tracker()

        elif choice == "3":
            print("Balance:", tracker.get_balance())

        elif choice == "4":
            transactions = tracker.get_transactions()
            if not transactions:
                print("No transactions yet.")
            else:
                print()
                for transaction in transactions:
                    print(transaction)

        elif choice == "5":
            print("Exiting program...")
            break

        elif choice == "6":
            summary = tracker.get_category_summary()
            if not summary:
                print("No expense data available.")
            else:
                print("\nCategory Spending Summary:")
                for category, total in summary.items():
                    print(f"{category}: ${total}")

        elif choice == "7":
            transactions = tracker.get_transactions()

            if not transactions:
                print("\nNo transactions to delete.")
                continue
            else:
                print()
                for transaction in transactions:
                    print(transaction)

                try:
                    transaction_id = int(input("\nEnter the ID of the transaction to delete: "))
                    delete_transaction(transaction_id)
                    refresh_tracker()
                    print("Transaction deleted successfully.")
                except ValueError:
                    print("Invalid ID. Please enter a valid transaction ID.")
                    continue

        elif choice == "8":
            transactions = tracker.get_transactions()

            if not transactions:
                print("No transactions to edit.")
                continue
            else:
                print()
                for transaction in transactions:
                    print(transaction)
                
                try:
                    transaction_id = int(input("\nEnter the ID of the transaction to edit: "))
                except ValueError:
                    print("Invalid ID. Please enter a valid transaction ID.")
                    continue
                
                selected_transaction = None

                for transaction in tracker.get_transactions():
                    if transaction.transaction_id == transaction_id:
                        selected_transaction = transaction
                        break
                
                if selected_transaction is None:
                    print("Transaction ID not found.")
                    continue

                new_type = input(f"Enter new type (leave blank if unchanged) [{selected_transaction.t_type}]: ").strip()
                if new_type == "":
                    new_type = selected_transaction.t_type

                new_amount = input(f"Enter new amount (leave blank if unchanged) [{abs(selected_transaction.amount)}]: ").strip()
                if new_amount == "":
                    amount = selected_transaction.amount
                else:
                    amount = float(new_amount)

                new_category = input(f"Enter new category (leave blank if unchanged) [{selected_transaction.category}]: ").strip()
                if new_category == "":
                    new_category = selected_transaction.category

                new_date = input(f"Enter new date (leave blank if unchanged) [{selected_transaction.date}]: ").strip()
                if new_date == "":
                    new_date = selected_transaction.date

                if new_type == "expense" and amount > 0:
                    amount = -amount
                elif new_type == "income" and amount < 0:
                    amount = abs(amount)

                updated_transaction = Transaction(amount, new_type, new_category, new_date, transaction_id)
                update_transaction(updated_transaction)
                refresh_tracker()
                print("Transaction updated successfully.")

        elif choice == "9":
            week_start = get_valid_date("Enter the start date of the week (YYYY-MM-DD): ")

            if week_start is None:
                continue

            summary = tracker.get_weekly_summary(week_start)
            print(f"\nWeekly Summary ({summary['week_start']} to {summary['week_end']}):")
            print(f"Total Income: ${summary['income']:.2f}")
            print(f"Total Expenses: ${summary['expenses']:.2f}")
            print(f"Net: ${summary['net']:.2f}")
            print(f"Projected Balance at End of Week: ${summary['projected_balance']:.2f}")

        elif choice == "10":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))

                if month < 1 or month > 12:
                    print("Invalid month. Please enter a value between 1 and 12.")
                    continue
            
            except ValueError:
                print("Invalid input. Please enter numeric values for year and month.")
                continue

            summary = tracker.get_monthly_summary(year, month)

            print(f"\nMonthly Summary ({year}-{month:02d}):")
            print(f"Total Income: ${summary['income']:.2f}")
            print(f"Total Expenses: ${summary['expenses']:.2f}")
            print(f"Net: ${summary['net']:.2f}")
            print(f"Projected Balance at End of Month: ${summary['projected_balance']:.2f}")

        elif choice == "11":
            transactions = create_recurring_transaction_set()

            if transactions is None:
                continue

            for transaction in transactions:
                save_transaction(transaction)

            refresh_tracker()

            print(
                f"\n{len(transactions)} recurring transactions created successfully."
            )

        else:
            print("Invalid choice. Please select 1-11.")

        

tracker = BudgetTracker()
create_table()
refresh_tracker()


run_app()

