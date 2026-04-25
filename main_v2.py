from datetime import date
import select

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


def create_transaction(t_type):
    amount = get_positive_amount()
    if amount is None:
        return None

    category = get_required_text("Enter category: ")
    if category is None:
        return None

    date = get_required_text("Enter date: ")
    if date is None:
        return None

    if t_type == "expense":
        amount = -amount
    print("DEBUG:", t_type, amount)    
    return Transaction(amount, t_type, category, date)


def show_menu():
    print("\n1. Add Income")
    print("2. Add Expense")
    print("3. Show Balance")
    print("4. Show Transactions")
    print("5. Exit")
    print("6. Show Category Summary")
    print("7. Delete Transaction")
    print("8. Edit Transaction")


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

        else:
            print("Invalid choice. Please select 1-8.")


tracker = BudgetTracker()
create_table()
refresh_tracker()


run_app()

