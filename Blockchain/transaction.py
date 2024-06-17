import hashlib
import base64

class Transaction:
    def __init__(self, senderPublicKey, sender, receiver, amount, signature=None):
        self.senderPublicKey = senderPublicKey
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def to_json(self):
        return {
            'senderPublicKey': base64.b64encode(self.senderPublicKey).decode('utf-8') if self.senderPublicKey else None,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'signature': self.signature
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            senderPublicKey=base64.b64decode(data['senderPublicKey']) if data['senderPublicKey'] else None,
            sender=data['sender'],
            receiver=data['receiver'],
            amount=data['amount'],
            signature=data['signature']
        )
    
    def calculate_hash(self):
        transaction_data = f'{self.sender}{self.receiver}{self.amount}'
        return hashlib.sha256(transaction_data.encode()).hexdigest()
    
    def __str__(self):
        return f'\nSender: {self.sender} \nsender Public Key{self.senderPublicKey} \nReceiver: {self.receiver}\n Amount: {self.amount} \nSignature: {self.signature}'

