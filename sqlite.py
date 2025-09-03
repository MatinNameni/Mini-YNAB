import sqlite3
from models import Transaction, Card

class WalletDAO:
    def __init__(self):
        self.conn = sqlite3.connect('Budget.db')
        self.c = self.conn.cursor()
    
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Wallet(
                        card_name TEXT PRIMARY KEY,
                        balance REAL
                      )''')
        
    def insert_card(self, card_name: str, balance: float):
        with self.conn:
            self.c.execute("INSERT INTO Wallet VALUES (:card_name, :balance)", {'card_name': card_name, 'balance': balance})
    
    def get_cards_name(self) -> list[str]:
        self.c.execute("SELECT card_name FROM Wallet")
        result = self.c.fetchall()
        cards = [card[0] for card in result]
        return cards
        
    def get_card(self, card_name: str) -> Card:
        self.c.execute("SELECT * FROM Wallet WHERE card_name = :card_name", {'card_name': card_name})
        result = self.c.fetchone()
        return Card(*result)

    def get_balance(self) -> float:
        #Return the total budget across all cards
        self.c.execute("SELECT SUM(balance) FROM Wallet")
        result = self.c.fetchone()
        return result[0] if result else 0.0
    
    def get_wallet(self) -> list[Card]:
        self.c.execute("SELECT * FROM Wallet")
        rows = self.c.fetchall()
        return [Card(*row) for row in rows]
    
    def edit_balance(self, card_name: str, new_balance: float):
        with self.conn:
            self.c.execute("""UPDATE Wallet SET balance = :balance
                           WHERE card_name = :card_name""",
                           {'balance': new_balance, 'card_name': card_name})
            
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        

class TransactionsDAO:
    def __init__(self):
        self.conn = sqlite3.connect('Budget.db')
        self.c = self.conn.cursor()
        
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Transactions(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        action_type TEXT,
                        card_name TEXT,
                        amount REAL,
                        category TEXT,
                        subcategory TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
        
    def insert_transaction(self, action_type: str, card_name: str, amount: float, category: str, subcategory: str):
        with self.conn:
            self.c.execute('''INSERT INTO Transactions (action_type, card_name, amount, category, subcategory)
                           VALUES (:action_type, :card_name, :amount, :category, :subcategory)''',
                           {'action_type': action_type, 'card_name': card_name, 'amount': amount,
                            'category': category, 'subcategory': subcategory})
            
    def get_all_transactions(self) -> list[Transaction]:
        self.c.execute("SELECT * FROM Transactions ORDER BY timestamp DESC")
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]

    def get_transactions_by_card(self, card_name: str) -> list[Transaction]:
        self.c.execute("""SELECT * FROM Transactions 
                       WHERE card_name = :card_name""",
                       {'card_name': card_name})
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]
    
    def get_transactions_by_type(self, action_type: str) -> list[Transaction]:
        self.c.execute("""SELECT * FROM Transactions 
                       WHERE action_type = :action_type""",
                       {'action_type': action_type})
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]
    
    def get_transactions_by_category(self, category: str) -> list[Transaction]:
        self.c.execute("""SELECT * FROM Transactions 
                       WHERE category = :category""",
                       {'category': category})
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]
    
    def get_transactions_by_date_range(self, range: str) -> list[Transaction]:
        date_ranges = {
            'Today': "start of day",
            'This Week': "start of week",
            'This Month': "start of month",
            'This Year': "start of year"
        }
        
        if range in date_ranges:
            self.c.execute("""SELECT * FROM Transactions 
                           WHERE DATE(timestamp) >= DATE('now', :range)""",
                           {'range': date_ranges[range]})
            rows = self.c.fetchall()
            return [Transaction(*row) for row in rows]
            
    def edit_category(self, id: int, new_category: str, new_subcategory: str):
        with self.conn:
            self.c.execute("""UPDATE Transactions SET category = :category, subcategory = :subcategory
                           WHERE id = :id""",
                           {'category': new_category, 'subcategory': new_subcategory, 'id': id})
            
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()