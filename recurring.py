from datetime import datetime, timedelta
import calendar

from transaction import create_signed_transaction


def add_month(date_obj, original_day):
    month = date_obj.month + 1
    year = date_obj.year

    if month > 12:
        month = 1
        year += 1

    last_day = calendar.monthrange(year, month)[1]
    
    day = min(original_day, last_day)

    return date_obj.replace(year=year, month=month, day=day)


def create_recurring_transactions(
    amount,
    t_type,
    category,
    start_date,
    frequency,
    repeats
):
    transactions = []

    current_date = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    ).date()

    original_day = current_date.day

    for _ in range(repeats):

        transaction = create_signed_transaction(
            amount,
            t_type,
            category,
            current_date.strftime("%Y-%m-%d")
        )

        transactions.append(transaction)

        if frequency == "weekly":
            current_date += timedelta(weeks=1)

        elif frequency == "biweekly":
            current_date += timedelta(weeks=2)

        elif frequency == "monthly":
            current_date = add_month(current_date, original_day)

    return transactions