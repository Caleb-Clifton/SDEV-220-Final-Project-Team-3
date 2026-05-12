from datetime import datetime, timedelta
import calendar
import transaction

def is_current_transaction(transaction_date):
        today = datetime.today().date()

        try:
            parsed_date = datetime.strptime(
                transaction_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return False

        return parsed_date <= today

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.balance = 0
        self.category_summary = {}

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        category = transaction.category.lower()

        if is_current_transaction(transaction.date):
            self.balance += transaction.amount

        # Display category spending as positive values for user experience, but store them as negative values for easier calculations
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
    
    # load/reload transactions to the program from the database any time a delete or edit transaction is made, and return them as a list of Transaction objects
    def load_transactions(self, transactions):
        self.transactions = []
        self.balance = 0
        self.category_summary = {}

        for transaction in transactions:
            self.add_transaction(transaction)

    def get_balance_by_date(self, end_date):
        total = 0

        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        for transaction in self.transactions:
            transaction_date = datetime.strptime(transaction.date, "%Y-%m-%d").date()

            if transaction_date <= end:
                total += transaction.amount

        return total
    
    def get_weekly_summary(self, week_start):
        income = 0
        expenses = 0

        start = datetime.strptime(week_start, "%Y-%m-%d").date()
        end = start + timedelta(days=6)

        for transaction in self.transactions:
            transaction_date = datetime.strptime(
                transaction.date,
                "%Y-%m-%d"
            ).date()

            if start <= transaction_date <= end:
                if transaction.t_type == "income":
                    income += transaction.amount
                elif transaction.t_type == "expense":
                    expenses += abs(transaction.amount)

        net = income - expenses
        projected_balance = self.get_balance_by_date(end.strftime("%Y-%m-%d"))

        return {
            "week_start": start,
            "week_end": end,
            "income": income,
            "expenses": expenses,
            "net": net,
            "projected_balance": projected_balance
        }
    
    def get_monthly_summary(self, year, month):
        income = 0
        expenses = 0

        start = datetime(year, month, 1).date()
        last_day = calendar.monthrange(year, month)[1]
        end = datetime(year, month, last_day).date()

        for transaction in self.transactions:
            transaction_date = datetime.strptime(
                transaction.date,
                "%Y-%m-%d"
            ).date()

            if start <= transaction_date <= end:
                if transaction.t_type == "income":
                    income += transaction.amount
                elif transaction.t_type == "expense":
                    expenses += abs(transaction.amount)

        net = income - expenses
        projected_balance = self.get_balance_by_date(end.strftime("%Y-%m-%d"))

        return {
            "month_start": start,
            "month_end": end,
            "income": income,
            "expenses": expenses,
            "net": net,
            "projected_balance": projected_balance
        }