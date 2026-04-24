class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.balance = 0
        self.category_summary = {}

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        # Expenses are stored as negative amounts, so we can just add them to the balance
        print("DEBUG in BudgetTracker:", transaction.t_type, transaction.amount)
        self.balance += transaction.amount
        print("DEBUG balance:", self.balance)
        category = transaction.category.lower()

        # Display category spending as potive values for user experience, but store them as negative values for easier calculations
        if transaction.t_type == "expense":
            if category in self.category_summary:
                self.category_summary[category] += abs(transaction.amount)
            else:
                self.category_summary[category] = abs(transaction.amount)

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions
    
    def get_category_summary(self):
        return self.category_summary
    