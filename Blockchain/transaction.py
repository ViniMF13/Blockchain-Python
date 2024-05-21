# blockchain/transaction.py
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __str__(self):
        return f"Transaction(sender={self.sender}, receiver={self.receiver}, amount={self.amount})"
