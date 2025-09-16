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
        if action_type == "Income":
            categories = list(CategoryManager().income_categories.keys())
        elif action_type == "Expense":
            categories = list(CategoryManager().expense_categories.keys())
        
        for i in range(len(categories)):
            print(f"{i+1}. {categories[i]}")
        category_index = int(input("Category number: "))
          
        return categories[category_index-1]
    
    def get_subcategory(self, category: str):
        if category in CategoryManager().income_categories:
            subcategories = list(CategoryManager().income_categories[category])
        else:
            subcategories = list(CategoryManager().expense_categories[category])

        for i in range(len(subcategories)):
            print(f"{i+1}. {subcategories[i]}")
        subcategory_index = int(input("Subcategory number: "))

        return subcategories[subcategory_index-1]
            
    def add_income(self):
        try:
            card_name = input("The card to which the money has been deposited: ")
            amount = float(input("Income amount: "))
            category = self.get_category("Income")
            subcategory = self.get_subcategory(category)
            date = input("date (format: YYYY-MM-DD | or enter 'today'): ")
            date = '' if date.lower() == 'today' else date
            self.finance_manager.income(card_name, amount, category, subcategory, date)
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
            category = self.get_category("Expense")
            subcategory = self.get_subcategory(category)
            date = input("date (format: YYYY-MM-DD | or enter 'today'): ")
            date = '' if date.lower() == 'today' else date
            self.finance_manager.expense(card_name, amount, category, subcategory, date)
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

    def manage_cards(self):
        try:
            print("1. Show Cards")
            print("2. Rename a Card")
            print("3. Remove a Card")
            print("0. Main Menu\n")
            choice = int(input("Choose an action: "))
            self.clear()
            match choice:
                case 1:
                    print(f"\n{self.wallet_manager.get_wallet()}")
                case 2:
                    card_name = input("Card name: ")
                    new_card_name = input("New card name: ")
                    self.wallet_manager.rename_card(card_name, new_card_name)
                    print("Card Renamed Successfully")
                case 3:
                    card_name = input("Card name: ")
                    confirm = input(f"Are you sure you want to delete {card_name}? (y/n): ")
                    if confirm.lower() == 'y':
                        self.wallet_manager.remove_card(card_name)
                        print("Card removed successfully")

        except CardNotFoundError as e:
            print(e)

        finally:
            input("Press any key to continue...")
            self.clear()
            self.run()

    def manage_transactions(self):
        try:
            print("1. Show transactions")
            print("2. Edit a transaction")
            print("3. Remove a transaction")
            print("0. Main Menu\n")
            choice = int(input("Choose an action: "))
            self.clear()
            match choice:
                case 1:
                    print("1. Show all")
                    print("2. Filter by card")
                    print("3. Filter by action")
                    print("4. Filter by category")
                    print("5. Filter by time")
                    print("0. Main Menu\n")
                    filter = int(input("Choose an action: "))
                    self.clear()
                    match filter:
                        case 1:
                            tr_list = self.transactions_dao.get_all()
                            print(self.transaction_manager.get_transictions(tr_list))

                        case 2:
                            card_name = input("Card name: ")
                            tr_list = self.transactions_dao.get_transactions_by_card(card_name)
                            print(self.transaction_manager.get_transictions(tr_list))

                        case 3:
                            action_type_handler = {
                                1: "Income",
                                2: "Expense"
                            }
                            print("1. Income")
                            print("2. Expense")
                            print("0. Main Menu\n")
                            action_type = int(input("Choose an action: "))
                            self.clear()
                            tr_list = self.transactions_dao.get_transactions_by_type(action_type_handler[action_type])
                            print(self.transaction_manager.get_transictions(tr_list))

                        case 4:
                            action_type_handler = {
                                1: "Income",
                                2: "Expense"
                            }
                            print("1. Income")
                            print("2. Expense")
                            print("0. Exit\n")
                            action_type = int(input("Choose an action: "))
                            self.clear()
                            category = self.get_category(action_type_handler[action_type])
                            tr_list = self.transactions_dao.get_transactions_by_category(category)
                            print(self.transaction_manager.get_transictions(tr_list))

                        case 5:
                            range_handler = {
                                1: "Today",
                                2: "This Week",
                                3: "This Month",
                                4: "This Year"
                            }
                            print("1. Today")
                            print("2. This Week")
                            print("3. This Month")
                            print("4. This Year")
                            print("0. Main Menu\n")
                            time_range = int(input("Choose an action: "))
                            tr_list = self.transactions_dao.get_transactions_by_date_range(range_handler[time_range])
                            print(self.transaction_manager.get_transictions(tr_list))

                case 2:
                    print("1. Edit Category")
                    print("2. Edit Date")
                    print("0. Main Menu")
                    choice = int(input("Choose an action: "))
                    self.clear()
                    match choice:
                        case 1:
                            tran_id = int(input("Transaction ID: "))
                            tran = self.transaction_manager.get_transaction_by_id(tran_id)
                            new_category = self.get_category(tran.action_type)
                            new_subcategory = self.get_subcategory(new_category)
                            self.transaction_manager.edit_category(tran_id, new_category, new_subcategory)
                            print("Category edited successfully")
                             
                        case 2:
                            tran_id = int(input("Transaction ID: "))
                            new_date = input("date (format: YYYY-MM-DD): ")
                            self.transaction_manager.edit_date(tran_id, new_date)
                            print("Date edited successfully")

                case 3:
                    tran_id = int(input("Transaction ID: "))
                    confirm = input("Are you sure you want to delete the transaction? (y/n): ")
                    if confirm.lower() == 'y':
                        self.finance_manager.remove_transaction(tran_id)
                        print("Transaction removed successfully")

        except CategoryNotFoundError as e:
            print(e)

        except TransactionNotFoundError as e:
            print(e)
        
        except InvalidDateFormatError as e:
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
                self.manage_cards()
            case 5:
                self.manage_transactions()
    
    def test_run(self):
        #print([int(*row) for row in self.transactions_dao.get_ids()])
        conn = sqlite3.connect("Budget.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Transactions WHERE DATE(Date) >= DATE('now', 'weekday 0', '-7 days')")
        l = c.fetchall()
        print(self.transaction_manager.get_transictions(l))
        conn.close()
    
if __name__ == "__main__":
    cli = CLI()
    cli.run()