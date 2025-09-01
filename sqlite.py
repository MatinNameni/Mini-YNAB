import sqlite3

class WalletDAO:
    def __init__(self):
        self.conn = sqlite3.connect('Wallet.db')
        self.c = self.conn.cursor()
    
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Wallet(
                        card_name TEXT PRIMARY KEY,
                        amount REAL
                      )''')
        
    def insert_card(self, card_name: str, amount: float):
        with self.conn:
            self.c.execute("INSERT INTO Wallet VALUES (:card_name, :amount)", {'card_name': card_name, 'amount': amount})
        
    def get_budget(self, card_name: str) -> float:
        #Return the budget for a given card. If not found, returns 0.0
        self.c.execute("SELECT amount FROM Wallet WHERE card_name = :card_name", {'card_name': card_name})
        result = self.c.fetchone()
        return result[0] if result else 0.0
    
    def edit_budget(self, card_name: str, new_amount: float):
        with self.conn:
            self.c.execute("""UPDATE Wallet SET amount = :amount
                           WHERE card_name = :card_name""",
                           {'amount': new_amount, 'card_name': card_name})
            
    def __enter__(self):
        return self

    def __exit__(self):
        self.close()