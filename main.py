from transaction import Transaction
from budget_tracker import BudgetTracker

tracker = BudgetTracker()

while True:
    print("\n1. Add Income")
    print("2. Add Expense")
    print("3. Show Balance")
    print("4. Show Transactions")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        date = input("Enter date: ")
        t = Transaction(amount, "income", category, date)
        tracker.add_transaction(t)

    elif choice == "2":
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        date = input("Enter date: ")
        t = Transaction(amount, "expense", category, date)
        tracker.add_transaction(t)

    elif choice == "3":
        print("Balance:", tracker.get_balance())

    elif choice == "4":
        for t in tracker.get_transactions():
            print(t)

    elif choice == "5":
        break

    else:
        print("Invalid choice")
          
