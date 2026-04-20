class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.balance = 0

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        if transaction.t_type == "income":
            self.balance += transaction.amount
        else:
            self.balance -= transaction.amount

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions
    