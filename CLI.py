import os
from main import *
from models import *
from sqlite import *

class CLI:
    def __init__(self):
        self.wallet_dao = WalletDAO()
        self.transactions_dao = TransactionsDAO()
        self.wallet_manager = WalletManager(self.wallet_dao)
        self.transaction_manager= TransactionManager(self.transactions_dao)
        self.finance_manager = FinanceManager(self.wallet_manager, self.transaction_manager)
        
    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
        
    def show_main_menu(self):
        print("\n===========================\n===Mini YNAB CLI version===\n===========================")
        print("1. Add Card")
        print("2. Add Income")
        print("3. Add Expense")
        print("4. Manage Cards")
        print("5. Manage Transactions")
        print("0. Exit\n")
    
    def add_card(self):
        try:
            card_name = input("Card name: ")
            balance = input("Card balance: ")
            self.wallet_manager.add_card(card_name, balance)
            print("Card added successfully")
            
        except CardAlreadyExistsError as e:
            print(e)
        
        finally:
            input("Press any key to continue...")
            self.clear()
            self.run()
            
    def get_category(self, action_type: str):
        if action_type == "income":
            categories = list(CategoryManager().income_categories.keys())
            subcategories = list(CategoryManager().income_categories.values())
        elif action_type == "expense":
            categories = list(CategoryManager().expense_categories.keys())
            subcategories = list(CategoryManager().expense_categories.values())
        
        for i in range(len(categories)):
            print(f"{i+1}. {categories[i]}")
        category_index = int(input("Category number: "))
        
        for i in range(len(subcategories[category_index-1])):
            print(f"{i+1}. {subcategories[category_index-1][i]}")
        subcategory_index = int(input("Subcategory number: "))
          
        return categories[category_index-1], subcategories[category_index-1][subcategory_index-1]
            
    def add_income(self):
        try:
            card_name = input("The card to which the money has been deposited: ")
            amount = float(input("Income amount: "))
            category, subcategory = self.get_category("income")
            self.finance_manager.income(card_name, amount, category, subcategory)
            print("Income added successfully")
            
        except CardNotFoundError as e:
            print(e)
        
        except CategoryNotFoundError as e:
            print(e)
            
        finally:
            input("Press any key to continue...")
            self.clear()
            self.run()
        
    def add_expense(self):
        try:
            card_name = input("The card from which the money was deducted: ")
            amount = float(input("Expense amount: "))
            category, subcategory = self.get_category("expense")
            self.finance_manager.expense(card_name, amount, category, subcategory)
            print("Expense added successfully")
            
        except CardNotFoundError as e:
            print(e)
            
        except NotEnoughBalanceError as e:
            print(e)
            
        except CategoryNotFoundError as e:
            print(e)
            
        finally:
            input("Press any key to continue...")
            self.clear()
            self.run()
    
    def run(self):
        self.show_main_menu()
        choice = int(input("Choose an action: "))
        self.clear()
        match choice:
            case 1:
                self.add_card()
            case 2:
                self.add_income()
            case 3:
                self.add_expense()
            case 4:
                pass
            case 5:
                pass
    
    def test_run(self):
        #self.finance_manager.income('Ansar', 120, 'Investments', 'Dividends')
        #self.finance_manager.expense('Ansar', 120, 'Shopping', 'Electronics')
        #print(self.transaction_manager.get_transictions())
        #self.wallet_manager.add_card('Saderat', 50)
        for i in range(len(list(CategoryManager().income_categories.keys()))):
            print(i)
    
if __name__ == "__main__":
    cli = CLI()
    cli.run()