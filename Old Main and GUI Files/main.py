from transaction import Transaction
from budget_tracker import BudgetTracker

tracker = BudgetTracker()

while True:
    print("\n1. Add Income")
    print("2. Add Expense")
    print("3. Show Balance")
    print("4. Show Transactions")
    print("5. Exit")
    print("6. Show Category Summary")

    choice = input("Choose an option: ")
    if choice == "1":
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than 0")
                continue
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            continue

        category = input("Enter category: ").strip()
        if category == "":
            print("Category cannot be empty")
            continue

        date = input("Enter date: ").strip()
        if date == "":
            print("Date cannot be empty")
            continue

        t = Transaction(amount, "income", category, date)
        tracker.add_transaction(t)

    
    elif choice == "2":
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than 0")
                continue
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            continue

        category = input("Enter category: ").strip()
        if category == "":
            print("Category cannot be empty")
            continue

        date = input("Enter date: ").strip()
        if date == "":
            print("Date cannot be empty")
            continue

        t = Transaction(amount, "expense", category, date)
        tracker.add_transaction(t)

    elif choice == "3":
        print("Balance:", tracker.get_balance())

   
    elif choice == "4":
        transactions = tracker.get_transactions()
        if not transactions:
            print("No transactions yet.")
        else:
            for t in transactions:
                print(t)

    
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