from main import *
from models import *
from sqlite import *

class CLI:
    def __init__(self):
        self.wallet_dao = WalletDAO()
        self.transactions_dao = TransactionsDAO()
        self.budget_manager = BudgetManager(self.wallet_dao)
        self.transaction_manager= TransactionManager(self.transactions_dao)
        self.finance_manager = FinanceManager(self.budget_manager, self.transaction_manager)
    
    def run(self):
        pass
    
    def test_run(self):
        #self.finance_manager.income('Ansar', 120, 'Investments', 'Dividends')
        #self.finance_manager.expense('Ansar', 120, 'Shopping', 'Electronics')
        print(self.budget_manager.show_wallet())
        self.budget_manager.add_card('Saderat', 50)
    
if __name__ == '__main__':
    cli = CLI()
    cli.test_run()