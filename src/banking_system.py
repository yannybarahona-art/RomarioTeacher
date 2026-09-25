import logging
from datetime import date


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
    _minimum_balance = 100
    def __init__(self, account_number, initial_balance=0):
        self._account_number = account_number
        self._currency = "USD"
        self._account_type = "Checking"
        self.__balance = initial_balance
        
        self._exchange_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "CRC": 600.0,
        }

    @property
    def account_number(self):
        return self._account_number

    @property
    def currency(self):
        return self._currency

    @property
    def account_type(self):
        return self._account_type

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        if value < 0:
           logging.error(f"Attempted to set negative balance: {value}")
           raise ValueError("Balance cannot be negative.")
        self.__balance = value
        logging.info(f"Balance updated to: {value}")
    @staticmethod    
    def is_valid_account_number(self, account_number):
        return isinstance(account_number, int) and len(str(account_number)) == 10
    @staticmethod
    def generate_account_number(self):
        import random
        return random.randint(1000000000, 9999999999)

    def minimum_balance(self,initial_balance):
        if initial_balance < self._minimum_balance:
            print(f"Initial balance {initial_balance} is less than minimum required balance {self._minimum_balance}")
            logging.error(f"Initial balance {initial_balance} is less than minimum required balance {self._minimum_balance}")
            raise ValueError("Initial balance cannot be less than minimum required balance.")



    def show_balance(self):
        print(f"Balance: {self.__balance}")

    def deposit(self, amount):
        if amount <=0:
            logging.error(f"The amount can't be negative {amount}")
            raise ValueError("Deposit amount must be positive.")
        self.__balance +=amount
        logging.info(f"Deposited {amount}. New balance: {self.__balance}")
        print(f"Deposited {amount}. New balance: {self.__balance}")

    def withdraw(self, amount):
        if amount <=0:
            logging.error(f"The amount can't be negative {amount}")
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            logging.error(f"Insufficient funds for withdrawal: {amount}. Current balance: {self.__balance}")
            raise InsufficientFundsError("Insufficient funds for withdrawal.", amount)
        if self.__balance - amount < self._minimum_balance:
            print(f"Withdrawal of {amount} would breach minimum balance. Current balance: {self.__balance}")
            logging.error(f"Withdrawal would breach minimum balance. Attempted withdrawal: {amount}. Current balance: {self.__balance}")
            raise ValueError("Withdrawal would breach minimum balance.")
            
            
        self.__balance -=amount
        logging.info(f"Withdrew {amount}. New balance: {self.__balance}")
        print(f"The amount {amount} has been withdrawn. New balance: {self.__balance}")                      
    def convert_currency(self, target_currency, exchange_rate):
        if target_currency == self._currency:
            logging.info(f"Currency conversion not needed. Already in {self._currency}.")
            return
        if target_currency not in self._exchange_rates:
            logging.error(f"Currency {target_currency} not supported for conversion.")
            raise ValueError(f"Currency {target_currency} not supported.")
        balance_converted = self.__balance * exchange_rate
        logging.info(f"Converted balance from {self._currency} to {target_currency}. New balance: {balance_converted}")
        print(f"Converted balance from {self._currency} to {target_currency}. New balance: {balance_converted}")
    @classmethod
    def create_saving(cls, balance):
        if balance < cls._minimum_balance:
            print(f"Saving account requires at least: {cls._minimum_balance}. Attempted to create with balance: {balance}")
            logging.error(f"Saving account requires at least: {cls._minimum_balance}. Attempted to create with balance: {balance}")
            raise ValueError("Initial balance cannot be negative.")
        account_number_generated = cls.generate_account_number(cls)
        return cls(account_number_generated, balance)
        
class Customer:
    user_id_count = 0
    def __init__(self, name, birth_date):
        Customer.user_id_count +=1
        self._user_id_count = Customer.user_id_count
        self._name = name
        self._birth_date = birth_date
        self.__accounts = []

    def validate_birth_date(self, birth_date):
        from datetime import date
        today = date.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age >= 18
    def add_account(self, account):
        if BankAccount.is_valid_account_number(self, account.account_number):
            self.__accounts.append(account)
            logging.info(f"Account {account.account_number} added for user {self._name}.")
            print(f"Account {account.account_number} added for user {self._name}.")

    def get_total_balance(self):
        total = sum(account.balance for account in self.__accounts)
        logging.info(f"Total balance for user {self._name}: {total}")
        print(f"Total balance for user 21 {self._name}: {total}")
        return total
        

try:
    account = BankAccount(100, 1000)
    #account.deposit(500)
    #account.balance = 50
    #account.withdraw(50)
    #account.convert_currency("EUR", 0.85)
    user=Customer("John Doe", "2008-09-28")
    user.validate_birth_date(date(2008,9,28))
    account = BankAccount.create_saving(190)
    user.add_account(account)
    print(f"Account {account.account_number} created for user {user._name} with balance {account.balance}.")
    print(f"Total balance for user {user._name}: {user.get_total_balance()}")
   
   
except ValueError as e:
    logging.error(f"Error: {e}") 
print(account.balance)
account.show_balance()