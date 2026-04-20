class Transaction:
    def __init__(self, amount, t_type, category, date):
        self.amount = amount
        self.t_type = t_type
        self.category = category
        self.date = date
    def __str__(self):
        return f"{self.t_type}: ${self.amount} - {self.category} on {self.date}"
