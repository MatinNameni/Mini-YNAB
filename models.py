from dataclasses import dataclass
import datetime
        
        
class CategoryManager:
    def __init__(self):
        self.income_categories = {
            'Salary': ['Monthly Salary', 'Bonus', 'Freelance'],
            'Investments': ['Dividends', 'Capital Gains', 'Interest'],
            'Gifts': ['From Family', 'From Friends', 'Other'],
            'Miscellaneous': ['Other']
        }
        
        self.expense_categories = {
            'Housing': ['Rent', 'Utilities', 'Maintenance'],
            'Food': ['Groceries', 'Dining Out', 'Coffee'],
            'Transportation': ['Public Transit', 'Fuel', 'Repairs'],
            'Entertainment': ['Movies', 'Concerts', 'Games'],
            'Health': ['Medical Bills', 'Pharmacy', 'Insurance'],
            'Shopping': ['Clothing', 'Electronics', 'Gifts'],
            'Savings': ['Emergency Fund', 'Retirement', 'Investments'],
            'Debt': ['Credit Card', 'Loans', 'Mortgage'],
            'Miscellaneous': ['Donations', 'Pet Care', 'Education', 'Other']
        }
    
    def is_category_correct(self, action_type: str, category: str, subcategory: str) -> bool:
        if action_type.lower() == 'income' and category.title() in self.income_categories:
            if subcategory.title() in self.income_categories[category.title()]:
                return True
        elif action_type.lower() == 'expense' and category.title() in self.expense_categories:
            if subcategory.title() in self.expense_categories[category.title()]:
                return True
        return False


@dataclass
class Card:
    name: str
    balance: float = 0.0
        

@dataclass
class Transaction:
    id: int | None
    action_type: str   # "Income" or "Expense"
    card_name: str
    amount: float
    category: str
    subcategory: str
    date: datetime.date | None = None