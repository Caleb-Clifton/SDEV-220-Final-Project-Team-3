from transaction import Transaction
from budget_tracker import BudgetTracker

tracker = BudgetTracker()


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


def run_app():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            transaction = create_transaction("income")
            if transaction:
                tracker.add_transaction(transaction)

        elif choice == "2":
            transaction = create_transaction("expense")
            if transaction:
                tracker.add_transaction(transaction)

        elif choice == "3":
            print("Balance:", tracker.get_balance())

        elif choice == "4":
            transactions = tracker.get_transactions()
            if not transactions:
                print("No transactions yet.")
            else:
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

        else:
            print("Invalid choice. Please select 1-6.")


run_app()

