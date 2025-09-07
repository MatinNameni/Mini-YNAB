from sqlite import WalletDAO, TransactionsDAO
from models import CategoryManager, Card, Transaction
from CustomExceptions import CardNotFoundError, CardAlreadyExistsError, NotEnoughBalanceError, CategoryNotFoundError

class WalletManager:
    def __init__(self, wallet: WalletDAO):
        self.wallet = wallet
        
    def add_card(self, card_name: str, balance: float = 0):
        with self.wallet as wallet:
            if card_name in wallet.get_cards_name():
                raise CardAlreadyExistsError(f"There is already a card with the name: {card_name}")
            wallet.insert(card_name, balance)
    
    def income(self, card_name: str, amount: float):
        with self.wallet as wallet:
            if card_name not in wallet.get_cards_name():
                raise CardNotFoundError(f"There is no card with the name: {card_name}")
            card = wallet.get_card(card_name)
            current_balance = card.balance
            new_balance = current_balance + amount
            wallet.edit_balance(card_name, new_balance)
    
    def expense(self, card_name: str, amount: float):
        with self.wallet as wallet:
            if card_name not in wallet.get_cards_name():
                raise CardNotFoundError(f"There is no card with the name {card_name}")
            card = wallet.get_card(card_name)
            current_balance = card.balance
            new_balance = current_balance - amount
            if new_balance < 0:
                raise NotEnoughBalanceError(f"{card_name} budget is short for {amount} amount of expense")
            wallet.edit_balance(card_name, new_balance)
    
    def get_wallet(self) -> str: #temporary function
        cards_list = ''
        with self.wallet as wallet:
            for card in wallet.get_all():
                cards_list += f'{card.name}: {card.balance}$\n'
        return cards_list
        
        
class TransactionManager:
    def __init__(self, transactions: TransactionsDAO):
        self.transactions = transactions
        
    def add_transaction(self, action_type: str, card_name: str, amount: float, category: str, subcategory: str):
        if CategoryManager().is_category_correct(action_type, category, subcategory):
            with self.transactions as transactions :
                transactions.insert(action_type, card_name, amount, category, subcategory)
        else:
            raise CategoryNotFoundError("Wrong input for category or subcategory")
    
    def get_transictions(self): #temporary function
        transictions_list = ''
        with self.transactions as transictions:
            for transiction in transictions.get_all():
                transictions_list += f'{transiction.id} {transiction.action_type} {transiction.card_name} {transiction.amount}$ {transiction.category} {transiction.subcategory} {transiction.timestamp}\n'
            return transictions_list
        
    def edit_category(self, id: int, category: str, subcategory: str):
        pass
    
    
class FinanceManager:
    def __init__(self, wallet: WalletManager, transactions: TransactionManager):
        self.wallet = wallet
        self.transactions = transactions
    
    def income(self, card_name: str, amount: float, category: str, subcategory: str):
        self.wallet.income(card_name, amount)
        self.transactions.add_transaction("income", card_name, amount, category, subcategory)
        
    def expense(self, card_name: str, amount: float, category: str, subcategory: str):
        self.wallet.expense(card_name, amount)
        self.transactions.add_transaction("expense", card_name, amount, category, subcategory)