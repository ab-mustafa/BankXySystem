"""
Unit tests for the `BankAccount` class.

This test suite covers:
- Bank Account Creation
- Withdraw from bank account operation
- Deposit into bank account operation
- Edge cases for withdraw and deposit operations
"""


import threading
import math
import pytest
from ..src.bank_account import BankAccount


class TestBankAccount:

    def test_Create_Bank_Account_With_Initial_Balance(self):
        """
            Test the bank account creation.
            This test ensures that the bank account created with initial balance
        """
        bankAccount = BankAccount(100.4)
        accountBalance = bankAccount.get_balance()
        assert math.isclose(accountBalance, 100.4)

    def test_Create_Bank_Account_With_Empty_Balance(self):
        bankAccount = BankAccount()
        accountBalance = bankAccount.get_balance()
        assert math.isclose(accountBalance, 0.0)

    def test_Create_Bank_Account_With_Zero_Balance(self):
        bankAccount = BankAccount(0.0)
        accountBalance = bankAccount.get_balance()
        assert math.isclose(accountBalance, 0.0)

    def test_Create_Bank_Account_With_invalid_Balance_Format(self):
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount("12.33")
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    def test_Create_Bank_Account_With_Negative_Balance(self):
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount(-50.20)
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    def test_Create_Bank_Account_With_Invalid_Balance(self):
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount("WWW")
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    def test_Create_Bank_Account_With_Balance_without_precision_digits(self):
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount(123)
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    # Deposit Test Cases
    def test_Deposit_money_from_the_Account(self):
        bankAccount = BankAccount(100.0)
        bankAccount.deposit(20.20)
        assert math.isclose(bankAccount.get_balance(), 120.2)

    def test_Deposit_Negative_amount_of_money_from_the_Account(self):
        bankAccount = BankAccount(50.5)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.deposit(-20.20)
        assert "Invalid transaction: Deposit in Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 50.5)

    def test_Deposit_Invalid_amount_of_money_from_the_Account(self):
        bankAccount = BankAccount(50.5)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.deposit("amount123")
        assert "Invalid transaction: Deposit in Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 50.5)

    def test_Deposit_to_Account_with_zero_balance(self):
        bankAccount = BankAccount()
        bankAccount.deposit(50.5)
        assert math.isclose(bankAccount.get_balance(), 50.5)

    # Withdraw Test Cases
    def test_Withdraw_from_account_amount_of_money_less_than_available_balance(self):
        bankAccount = BankAccount(120.50)
        bankAccount.withdraw(50.5)
        assert math.isclose(bankAccount.get_balance(), 70.0)

    def test_Withdraw_from_account_amount_of_money_more_than_available_balance(self):
        bankAccount = BankAccount(120.50)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.withdraw(150.0)
        assert "Invalid transaction: Withdraw amount more than of the available balance not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 120.50)

    def test_Withdraw_from_account_invalid_amount_of_money(self):
        bankAccount = BankAccount(120.50)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.withdraw("123W")
        assert "Invalid transaction: Withdraw from Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 120.50)

    def test_Withdraw_from_account_negative_amount_of_money(self):
        bankAccount = BankAccount(120.50)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.withdraw(-12.5)
        assert "Invalid transaction: Withdraw from Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 120.50)

    def test_Withdraw_all_available_balance_from_account(self):
        bankAccount = BankAccount(120.50)
        bankAccount.withdraw(120.50)
        assert math.isclose(bankAccount.get_balance(), 0.0)

    def test_Verify_that_Balance_variable_is_thread_safe(self):
        account = BankAccount(120.0)

        def task_withdraw_ten_times(bankAccount: BankAccount):
            for i in range(10):
                bankAccount.withdraw(5.0)

        def task_Deposit_ten_times(bankAccount: BankAccount):
            for i in range(10):
                bankAccount.deposit(5.0)

        thread1 = threading.Thread(target=task_Deposit_ten_times(account), name='t1')
        thread2 = threading.Thread(target=task_withdraw_ten_times(account), name='t2')
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        assert account.get_balance() == 120.0
