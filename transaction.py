from datetime import datetime

class Transaction:
    def __init__(self, amount, t_type, category, date, transaction_id=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.t_type = t_type
        self.category = category
        self.date = date

    def __str__(self):
        today = datetime.today().date()

        transaction_date = datetime.strptime(
            self.date,
            "%Y-%m-%d"
        ).date()

        status = "FUTURE" if transaction_date > today else "CURRENT"

        return (
            f"ID:{self.transaction_id} | "
            f"{status} | "
            f"{self.t_type}: "
            f"${self.amount:.2f} - "
            f"{self.category} on {self.date}"
        )

# Added this function in transaction.py to be called by gui file
def create_signed_transaction(amount, t_type, category, date, transaction_id=None):
    if t_type == "expense" and amount > 0:
        amount = -amount
    elif t_type == "income" and amount < 0:
        amount = abs(amount)

    return Transaction(amount, t_type, category, date, transaction_id)