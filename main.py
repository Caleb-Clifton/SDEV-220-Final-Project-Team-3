from transaction import Transaction
from budget_tracker import BudgetTracker

tracker = BudgetTracker()

t1 = Transaction(1000, "income", "job", "2026-04-15")
t2 = Transaction(200, "expense", "food","2026-04-15")

tracker.add_transaction(t1)
tracker.add_transaction(t2)

print("Balance:", tracker.get_balance())
