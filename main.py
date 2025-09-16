from sqlite import WalletDAO, TransactionsDAO
from models import CategoryManager, Card, Transaction
from CustomExceptions import *
import datetime
from tabulate import tabulate
    

class WalletManager:
    def __init__(self, wallet: WalletDAO):
        self.wallet = wallet
        
    def add_card(self, card_name: str, balance: float = 0):
        if card_name in self.wallet.get_cards_name():
            raise CardAlreadyExistsError(f"There is already a card with the name: {card_name}")
        self.wallet.insert(card_name, balance)

    def remove_card(self, card_name: str):
        if card_name not in self.wallet.get_cards_name():
            raise CardNotFoundError(f"There is no card with the name: {card_name}")
        self.wallet.remove(card_name)

    def rename_card(self, card_name: str, new_card_name:str):
        if card_name not in self.wallet.get_cards_name():
            raise CardNotFoundError(f"There is no card with the name: {card_name}")
        card = self.wallet.get_card(card_name)
        self.wallet.edit(card_name=card.name, new_card_name=new_card_name, new_balance=card.balance)
             
    def income(self, card_name: str, amount: float):
        if card_name not in self.wallet.get_cards_name():
            raise CardNotFoundError(f"There is no card with the name: {card_name}")
        card = self.wallet.get_card(card_name)
        current_balance = card.balance
        new_balance = current_balance + amount
        self.wallet.edit(card_name=card.name, new_card_name=card.name, new_balance=new_balance)
    
    def expense(self, card_name: str, amount: float):
        if card_name not in self.wallet.get_cards_name():
            raise CardNotFoundError(f"There is no card with the name {card_name}")
        card = self.wallet.get_card(card_name)
        current_balance = card.balance
        new_balance = current_balance - amount
        if new_balance < 0:
            raise NotEnoughBalanceError(f"{card_name} budget is short for {amount} amount of expense")
        self.wallet.edit(card_name=card_name, new_card_name=card_name, new_balance=new_balance)
    
    def get_wallet(self) -> str:
        cards = self.wallet.get_all()
        headers = ["CardName", "Balance"]
        return tabulate(cards, headers, tablefmt="grid")


class TransactionManager:
    def __init__(self, transactions: TransactionsDAO):
        self.transactions = transactions
        
    def add_transaction(self, action_type: str, card_name: str, amount: float, category: str, subcategory: str, date: str):
        if CategoryManager().is_category_correct(action_type, category, subcategory):
            self.transactions.insert(action_type, card_name, amount, category, subcategory, date)
        else:
            raise CategoryNotFoundError("Wrong input for category or subcategory")
    
    def get_transaction_by_id(self, id) -> Transaction:
        if id not in self.transactions.get_ids():
            raise TransactionNotFoundError("Transaction not found")
        return self.transactions.get_transaction_by_id(id)
    
    def get_transictions(self, transactons_list: list[Transaction]) -> str:
        headers = ["ID", "ActionType", "CardName", "Amount", "Category", "Subcategory", "Date"]
        return tabulate(transactons_list, headers, tablefmt="grid")

    def remove_transaction(self, id: int) -> Transaction:
        removed_tran = self.get_transaction_by_id(id)
        self.transactions.remove(id)
        return removed_tran
        
    def edit_category(self, id: int, new_category: str, new_subcategory: str):
        tran = self.get_transaction_by_id(id)
        if CategoryManager().is_category_correct(tran.action_type, new_category, new_subcategory) == False:
            raise CategoryNotFoundError("Wrong input for category or subcategory")
        self.transactions.edit(id, new_category, new_subcategory, tran.date)

    def edit_date(self, id: int, new_date: str):
        tran = self.get_transaction_by_id(id)
        try:
            if bool(datetime.date.fromisoformat(new_date)):
                self.transactions.edit(id, tran.category, tran.subcategory, new_date)
        except ValueError:
            raise InvalidDateFormatError("Date format is not correct")
    
    
class FinanceManager:
    def __init__(self, wallet_manager: WalletManager, tran_manager: TransactionManager):
        self.wallet_manager = wallet_manager
        self.tran_manager = tran_manager
    
    def income(self, card_name: str, amount: float, category: str, subcategory: str, date: str):
        self.wallet_manager.income(card_name, amount)
        self.tran_manager.add_transaction("Income", card_name, amount, category, subcategory, date)
        
    def expense(self, card_name: str, amount: float, category: str, subcategory: str, date: str):
        self.wallet_manager.expense(card_name, amount)
        self.tran_manager.add_transaction("Expense", card_name, amount, category, subcategory, date)

    def remove_transaction(self, id: int):
        removed_tran = self.tran_manager.remove_transaction(id)
        if removed_tran.action_type == "Income":
            self.wallet_manager.expense(removed_tran.card_name, removed_tran.amount)
        else:
            self.wallet_manager.income(removed_tran.card_name, removed_tran.amount)