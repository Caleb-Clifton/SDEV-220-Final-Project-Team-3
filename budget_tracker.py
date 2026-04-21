class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.balance = 0
        self.category_summary = {}

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        if transaction.t_type == "income":
            self.balance += transaction.amount
        else:
            self.balance -= transaction.amount
        category = transaction.category.lower()
        if transaction.t_type == "expense":
            if category in self.category_summary:
                self.category_summary[category] += transaction.amount
            else:
                self.category_summary[category] = transaction.amount

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions
    
    def get_category_summary(self):
        return self.category_summary
    