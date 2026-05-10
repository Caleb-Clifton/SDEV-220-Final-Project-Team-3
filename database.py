import sqlite3
from transaction import Transaction

def connect_db():
    conn = sqlite3.connect("budget.db")
    return conn

# create table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            t_type TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# save a transaction to the database from the program
def save_transaction(transaction):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (amount, t_type, category, date)
        VALUES (?, ?, ?, ?)
    ''', (transaction.amount, transaction.t_type, transaction.category, transaction.date))
    conn.commit()
    conn.close()

# load transactions to the program from the database when the program starts up, and return them as a list of Transaction objects
def load_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()

    conn.close()

    transaction_list = []

    for row in rows:
        transaction = Transaction(
            row[1],  # amount
            row[2],  # t_type
            row[3],  # category
            row[4],  # date
            row[0]   # transaction_id
        )
        transaction_list.append(transaction)
    
    return transaction_list

# delete a transaction from the database by its ID
def delete_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))

    conn.commit()
    conn.close()

# update a transaction in the database by its ID
def update_transaction(transaction):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE transactions
        SET amount = ?, t_type = ?, category = ?, date = ?
        WHERE id = ?
    ''', (transaction.amount, transaction.t_type, transaction.category, transaction.date, transaction.transaction_id))

    conn.commit()
    conn.close()
