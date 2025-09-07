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
        return self.message


class CardAlreadyExistsError(WalletError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return self.message

  
class NotEnoughBalanceError(WalletError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return self.message
    
    
class CategoryNotFoundError(TransactionError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return self.message