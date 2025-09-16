class AppError(Exception):
    pass


class WalletError(AppError):
    pass


class TransactionError(AppError):
    pass


class CardNotFoundError(WalletError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return f'CardNotFoundError: {self.message}'


class CardAlreadyExistsError(WalletError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return f'CardAlreadyExistsError: {self.message}'

  
class NotEnoughBalanceError(WalletError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return f'NotEnoughBalanceError: {self.message}'
    
    
class CategoryNotFoundError(TransactionError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return f'TransactionNotFoundError: {self.message}'
    

class TransactionNotFoundError(TransactionError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return f'TransactionNotFoundError: {self.message}'
    

class InvalidDateFormatError(TransactionError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return f'InvalidDateFormatError: {self.message}'