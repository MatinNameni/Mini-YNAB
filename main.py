from sqlite import WalletDAO, TransactionsDAO
from models import CategoryManager

class BudgetManager:
    def __init__(self, wallet: WalletDAO):
        self.wallet = wallet
        
    def add_card(self, card_name: str, balance: float = 0):
        with self.wallet as wallet:
            wallet.insert_card(card_name, balance)
    
    def income(self, card_name: str, amount: float):
        with self.wallet as wallet:
            if card_name in wallet.get_cards_name():
                card = wallet.get_card(card_name)
                current_balance = card.balance
                new_balance = current_balance + amount
                wallet.edit_balance(card_name, new_balance)
            else:
                raise ValueError(f"there is no card with the name {card_name}")
            
    
    def expense(self, card_name: str, amount: float) -> bool:
        with self.wallet as wallet:
            if card_name in wallet.get_cards_name():
                card = wallet.get_card(card_name)
                current_balance = card.balance
                new_balance = current_balance - amount
                if new_balance >= 0:
                    wallet.edit_balance(card_name, new_balance)
                    return True
                return False
            else:
                raise ValueError(f"there is no card with the name {card_name}")
    
    def show_wallet(self) -> str:
        cards = ''
        with self.wallet as wallet:
            for card in wallet.get_wallet():
                cards += f'{card.name}: {card.balance}\n'
        return cards
        
class TransactionManager:
    def __init__(self, transactions : TransactionsDAO):
        self.transactions = transactions
        
    def add_transaction(self, action_type: str, card_name: str, amount: float, category: str, subcategory: str):
        if CategoryManager().is_category_correct(action_type, category, subcategory):
            with self.transactions as transactions :
                transactions.insert_transaction(action_type, card_name, amount, category, subcategory)
        else:
            raise ValueError("Input is not correct.")
    
    def get_transictions(self, filter: str):
        pass
        
    def edit_category(self, id: int, category: str, subcategory: str):
        pass
    
class FinanceManager:
    def __init__(self, budget: BudgetManager, transactions: TransactionManager):
        self.budget = budget
        self.transactions = transactions
    
    def income(self, card_name: str, amount: float, category: str, subcategory: str):
        self.budget.income(card_name, amount)
        self.transactions.add_transaction("income", card_name, amount, category, subcategory)
        
    def expense(self, card_name: str, amount: float, category: str, subcategory: str):
        if self.budget.expense(card_name, amount):
            self.transactions.add_transaction("expense", card_name, amount, category, subcategory)
        else:
            pass
            #raise ??error