from sqlite import WalletDAO

class BudgetManager:
    def __init__(self, wallet: WalletDAO):
        self.wallet = wallet
    
    def income(self, card_name: str, amount: float):
        with self.wallet as wallet:
            current_budget = wallet.get_budget(card_name)
            new_budget = current_budget + amount
            wallet.edit_budget(card_name, new_budget)
            
    
    def expense(self, card_name: str, amount: float) -> bool:
        with self.wallet as wallet:
            current_budget = wallet.get_budget(card_name)
            new_budget = current_budget - amount
            if new_budget >= 0:
                wallet.edit_budget(card_name, new_budget)
                return True
            return False