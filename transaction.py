class Transaction:
    def __init__(self, amount, t_type, category, date, transaction_id=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.t_type = t_type
        self.category = category
        self.date = date
    def __str__(self):
        return f"ID:{self.transaction_id} |  {self.t_type}: ${self.amount:.2f} - {self.category} on {self.date}"
