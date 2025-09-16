import sqlite3
from abc import ABC, abstractmethod
from models import Transaction, Card
from typing import Any

class DatabaseConnectionManager:
    _instance = None
    
    def __new__(cls, db_path: str = 'Budget.db'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = db_path
        return cls._instance
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


class BaseDAO(ABC):
    @abstractmethod
    def create_table(self):
        pass
    
    @abstractmethod
    def insert(self, *args):
        pass

    @abstractmethod
    def remove(self, *args):
        pass

    @abstractmethod
    def edit(self, *args):
        pass
    
    @abstractmethod
    def get_all(self) -> list[Any]:
        pass


class WalletDAO(BaseDAO):
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
        self.conn = self.db_manager.get_connection()
        self.c = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Wallet(
                        CardName TEXT PRIMARY KEY,
                        Balance REAL
                      )''')
        self.conn.commit()
        
    def insert(self, card_name: str, balance: float):
        self.c.execute("INSERT INTO Wallet VALUES (:card_name, :balance)", {'card_name': card_name, 'balance': balance})
        self.conn.commit()
            
    def remove(self, card_name: str):
        self.c.execute("""DELETE FROM Wallet
                       WHERE CardName = :card_name""",
                       {"card_name": card_name})
        self.conn.commit()

    def edit(self, card_name: str, new_card_name: str, new_balance: float):
        self.c.execute("""UPDATE Wallet SET CardName = :new_card_name, Balance = :new_balance
                        WHERE CardName = :card_name""",
                        {'new_card_name': new_card_name, 'new_balance': new_balance, 'card_name': card_name})
        self.conn.commit()
            
    def get_all(self) -> list[Card]:
        self.c.execute("SELECT * FROM Wallet")
        rows = self.c.fetchall()
        return [Card(*row) for row in rows]
    
    def get_cards_name(self) -> list[str]:
        self.c.execute("SELECT CardName FROM Wallet")
        result = self.c.fetchall()
        cards = [card[0] for card in result]
        return cards
        
    def get_card(self, card_name: str) -> Card:
        self.c.execute("SELECT * FROM Wallet WHERE CardName = :card_name", {'card_name': card_name})
        result = self.c.fetchone()
        return Card(*result)

    def get_total_balance(self) -> float:
        #Return the total budget across all cards
        self.c.execute("SELECT SUM(Balance) FROM Wallet")
        result = self.c.fetchone()
        return result[0] if result else 0.0
    

class TransactionsDAO(BaseDAO):
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
        self.conn = self.db_manager.get_connection()
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS Transactions(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ActionType TEXT,
                    CardName TEXT,
                    Amount REAL,
                    Category TEXT,
                    Subcategory TEXT,
                    Date DATE DEFAULT CURRENT_DATE
                  )""")
        self.conn.commit()
        
    def insert(self, action_type: str, card_name: str, amount: float, category: str, subcategory: str, date: str = None):
        if date:
            self.c.execute("""INSERT INTO Transactions (ActionType, CardName, Amount, Category, Subcategory, Date)
                            VALUES (:action_type, :card_name, :amount, :category, :subcategory, :date)""",
                            {'action_type': action_type, 'card_name': card_name, 'amount': amount,
                            'category': category, 'subcategory': subcategory, 'date': date})
        else:
            self.c.execute("""INSERT INTO Transactions (ActionType, CardName, Amount, Category, Subcategory)
                            VALUES (:action_type, :card_name, :amount, :category, :subcategory)""",
                            {'action_type': action_type, 'card_name': card_name, 'amount': amount,
                            'category': category, 'subcategory': subcategory})
        self.conn.commit()

    def edit(self, id: int, new_category: str, new_subcategory: str, new_date: str):
        self.c.execute("""UPDATE Transactions SET Category = :new_category, Subcategory = :new_subcategory, Date = :new_date
                       WHERE ID = :id""",
                       {'new_category': new_category, 'new_subcategory': new_subcategory, 'new_date': new_date, 'id': id})
        self.conn.commit()

    def remove(self, id: int):
        self.c.execute("""DELETE FROM Transactions
                       WHERE ID = :id""",
                       {"id": id})
        self.conn.commit()

            
    def get_all(self) -> list[Transaction]:
        self.c.execute("SELECT * FROM Transactions ORDER BY Date ASC")
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]
    
    def get_ids(self) -> list[int]:
        self.c.execute("SELECT ID FROM Transactions")
        ids =  self.c.fetchall()
        return [int(*id) for id in ids]
    
    def get_transaction_by_id(self, id: int) -> Transaction:
        self.c.execute("SELECT * FROM Transactions WHERE ID = :id", {"id": id})
        tran = self.c.fetchone()
        return Transaction(*tran)

    def get_transactions_by_card(self, card_name: str) -> list[Transaction]:
        self.c.execute("""SELECT * FROM Transactions 
                       WHERE CardName = :card_name""",
                       {'card_name': card_name})
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]
    
    def get_transactions_by_type(self, action_type: str) -> list[Transaction]:
        self.c.execute("""SELECT * FROM Transactions 
                       WHERE ActionType = :action_type""",
                       {'action_type': action_type})
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]
    
    def get_transactions_by_category(self, category: str) -> list[Transaction]:
        self.c.execute("""SELECT * FROM Transactions 
                       WHERE Category = :category""",
                       {'category': category})
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]
    
    def get_transactions_by_date_range(self, range: str) -> list[Transaction]:
        date_ranges = {
            'Today': "start of day",
            'This Month': "start of month",
            'This Year': "start of year"
        }
        
        if range in date_ranges:
            self.c.execute("""SELECT * FROM Transactions
                           WHERE DATE(Date) >= DATE('now', :range)""",
                           {'range': date_ranges[range]})
        elif range == "This Week":
            self.c.execute("""SELECT * FROM Transactions
                           WHERE DATE(Date) >= DATE('now', 'weekday 0', '-7 days')""")
        rows = self.c.fetchall()
        return [Transaction(*row) for row in rows]