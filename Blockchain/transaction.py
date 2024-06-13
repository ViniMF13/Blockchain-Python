import hashlib

class Transaction:
    def __init__(self, senderPublicKey, sender, receiver, amount):
        self.senderPublicKey = senderPublicKey
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def calculate_hash(self):
        transaction_data = f'{self.sender}{self.receiver}{self.amount}'
        return hashlib.sha256(transaction_data.encode()).hexdigest()
    
    def __str__(self):
        return f'\nSender: {self.sender} \nsender Public Key{self.senderPublicKey} \nReceiver: {self.receiver}\n Amount: {self.amount} \nSignature: {self.signature}'

