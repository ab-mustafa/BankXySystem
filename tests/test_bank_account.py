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
        """
            Test the bank account creation.
            This test ensures that the  bank account balance should be
             Zero when balance paramter is empty.
        """
        bankAccount = BankAccount()
        accountBalance = bankAccount.get_balance()
        assert math.isclose(accountBalance, 0.0)

    def test_Create_Bank_Account_With_Zero_Balance(self):
        """
        Test the bank account creation.
        This test ensures that the  bank account balance can be created with balance equal zero.
        """
        bankAccount = BankAccount(0.0)
        accountBalance = bankAccount.get_balance()
        assert math.isclose(accountBalance, 0.0)

    def test_Create_Bank_Account_With_invalid_Balance_Format(self):
        """
            Test the bank account creation.
            This test ensures that the  bank account can't be created when the balance variable type not float.
        """
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount("12.33")
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    def test_Create_Bank_Account_With_Negative_Balance(self):
        """
            Test the bank account creation.
            This test ensures that the  bank account can't be created when the initial balance is negative.
        """

        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount(-50.20)
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    def test_Create_Bank_Account_With_Invalid_Balance(self):
        """
            Test the bank account creation.
            This test ensures that the  bank account can't be created when the initial balance is a string.
        """
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount("WWW")
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    def test_Create_Bank_Account_With_Balance_without_precision_digits(self):
        """
            Test the bank account creation.
            This test ensures that the  bank account can't be created when the initial balance is integer.
        """
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount = BankAccount(123)
        assert "Invalid transaction: Creating Account with Invalid Balance not permitted." in str(exceptionInfo.value)

    # Deposit Test Cases
    def test_Deposit_money_from_the_Account(self):
        """
            Test bank account deposit operation.
            This test ensures that the bank account can perform deposit operation.
            Scenario: Bank account created with initial balance 100.0$ and a deposit operation created to this account
            with value 20.20$
            Expected: The bank account balance should be 120.2 after deposit operation.
        """
        bankAccount = BankAccount(100.0)
        bankAccount.deposit(20.20)
        assert math.isclose(bankAccount.get_balance(), 120.2)

    def test_Deposit_Negative_amount_of_money_from_the_Account(self):
        """
            Test bank account deposit operation.
            This test ensures that the deposit operation can't be performed when the deposit is a negative value.
            Scenario: Bank account created with initial balance 50.0$ and a deposit operation created to this account
            with value -20.20$
            Expected: The deposit operation should be suspended, and the account balance should not be changed and the balance should be equal 50.5$.
        """

        bankAccount = BankAccount(50.5)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.deposit(-20.20)
        assert "Invalid transaction: Deposit in Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 50.5)

    def test_Deposit_Invalid_amount_of_money_from_the_Account(self):
        """
            Test bank account deposit operation.
            This test ensures that the bank account can't perform deposit operation when the deposit value type not float.
            Scenario: Bank account created with initial balance 100.0$ and a deposit operation created to this account
            with Invalid variable type lik string.
            Expected: The deposit operation should be suspended, and the bank account balance should be 50.5 after deposit operation.
        """
        bankAccount = BankAccount(50.5)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.deposit("amount123")
        assert "Invalid transaction: Deposit in Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 50.5)

    def test_Deposit_to_Account_with_zero_balance(self):
        """
            Test bank account deposit operation.
            This test ensures that the bank account can perform deposit operation in a account with balance zero.
            Scenario: Bank account created with initial balance 0.0$ and a deposit operation created to this account
            with $50.5.
            Expected: The deposit operation should be created, and the bank account balance should be 50.5 after deposit operation.
        """

        bankAccount = BankAccount()
        bankAccount.deposit(50.5)
        assert math.isclose(bankAccount.get_balance(), 50.5)

    # Withdraw Test Cases
    def test_Withdraw_from_account_amount_of_money_less_than_available_balance(self):
        """
            Test bank account withdraw operation.
            This test ensures that the bank account can perform withdraw operation.
            Scenario: Bank account created with initial balance $120.50 and a withdraw operation created to this account
            with $50.5.
            Expected: The withdraw operation should be created, and the bank account balance should be 70.0 after withdraw operation.
        """
        bankAccount = BankAccount(120.50)
        bankAccount.withdraw(50.5)
        assert math.isclose(bankAccount.get_balance(), 70.0)

    def test_Withdraw_from_account_amount_of_money_more_than_available_balance(self):
        """
            Test bank account withdraw operation.
            This test ensures that the bank account can't perform withdraw operation more than the available balance.
            Scenario: Bank account created with initial balance $120.50 and a withdraw operation created to this account
            with $150.0.
            Expected: The withdraw operation should be suspended, and the bank account balance should not be changed after withdraw operation.
        """
        bankAccount = BankAccount(120.50)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.withdraw(150.0)
        assert "Invalid transaction: Withdraw amount more than of the available balance not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 120.50)

    def test_Withdraw_from_account_invalid_amount_of_money(self):
        """
           Test bank account withdraw operation.
           This test ensures that the bank account can't perform withdraw operation when that value is not float.
            Scenario: Bank account created with initial balance $120.50 and a withdraw operation created to this account
            with string type.
            Expected: The withdraw operation should be suspended, and the bank account balance should not be changed after withdraw operation.
        """
        bankAccount = BankAccount(120.50)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.withdraw("123W")
        assert "Invalid transaction: Withdraw from Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 120.50)

    def test_Withdraw_from_account_negative_amount_of_money(self):
        """
            Test bank account withdraw operation.
            This test ensures that the bank account can't perform withdraw operation with a negative value.
            Scenario: Bank account created with initial balance $120.50 and a withdraw operation created to this account
            with $-12.5.
            Expected: The withdraw operation should be suspended, and the bank account balance should not be changed after withdraw operation.
        """
        bankAccount = BankAccount(120.50)
        with pytest.raises(ValueError) as exceptionInfo:
            bankAccount.withdraw(-12.5)
        assert "Invalid transaction: Withdraw from Account with Invalid money amount not permitted." in str(
            exceptionInfo.value)
        assert math.isclose(bankAccount.get_balance(), 120.50)

    def test_Withdraw_all_available_balance_from_account(self):
        """
            Test bank account withdraw operation.
            This test ensures that the bank account can perform withdraw operation to withdraw all available balance.
            Scenario: Bank account created with initial balance $120.50 and a withdraw operation created to this account
            with $120.5.
            Expected: The withdraw operation should be successful, and the bank account balance should be equal zero.
        """
        bankAccount = BankAccount(120.50)
        bankAccount.withdraw(120.50)
        assert math.isclose(bankAccount.get_balance(), 0.0)

    def test_Verify_that_Balance_variable_is_thread_safe(self):
        """
            Test bank account balance is thread safe.
            This test ensures that the bank account balance is thread safe when there is multiple thread are perform operation at the
            same time in the same bank account.
            Scenario: Bank account created with initial balance $120.50 and a 10 withdraw operation created to this account with $5 value, and
            a 10 deposit operation executed in the same account in the same time with value $5.

            Expected: The Account balance should be $120.0.
        """
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
