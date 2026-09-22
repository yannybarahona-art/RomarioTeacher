import logging



logging.basicConfig(
    filename="bank_system.log",
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(message)s",
    )

class InsufficientFundsError(Exception):
    def __init__(self, message, withdrawal_amount):
        self.withdrawal_amount = withdrawal_amount
        super().__init__(message)
class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.currency = "USD"
        self._account_type = "Checking"
        self.__balance = 0.0


      