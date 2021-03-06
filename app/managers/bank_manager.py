import enum


class FormParametersForBank(enum.Enum):
    bank_number = 'bank_number'
    amount = 'amount'
    user_id = 'user_id'


class BankInfo:
    def __init__(self, bank_id, amount, bank_number, user_id):
        self.bank_id = bank_id
        self.amount = amount
        self.bank_number = bank_number
        self.user_id = user_id

