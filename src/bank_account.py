import threading


class BankAccount:
    def __init__(self, initial_balance: float = 0.0):
        if not self.__Verify_balance_value(initial_balance):
            raise ValueError("Invalid transaction: Creating Account with Invalid Balance not permitted.")

        self._balance = round(initial_balance, 2)
        self.lock = threading.Lock()

    def deposit(self, amount: float):
        if not self.__Verify_balance_value(amount):
            raise ValueError("Invalid transaction: Deposit in Account with Invalid money amount not permitted.")
        with self.lock:
            self._balance += round(amount, 2)

    def withdraw(self, amount: float):
        if not self.__Verify_balance_value(amount):
            raise ValueError("Invalid transaction: Withdraw from Account with Invalid money amount not permitted.")
        elif round(amount, 2) > self._balance:
            raise ValueError("Invalid transaction: Withdraw amount more than of the available balance not permitted.")

        with self.lock:
            self._balance -= round(amount, 2)

    def get_balance(self) -> float:
        return self._balance

    def __Verify_balance_value(self, balance_value):
        if isinstance(balance_value, float) and balance_value >= 0.0:
            return True
        return False
