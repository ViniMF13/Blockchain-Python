import hashlib
import json
import ecdsa

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def calculate_hash(self):
        transaction_data = f'{self.sender}{self.receiver}{self.amount}'
        return hashlib.sha256(transaction_data.encode()).hexdigest()

    def sign_transaction(self, signing_key):
        if signing_key.get_verifying_key().to_string().hex() != self.sender:
            raise ValueError("You cannot sign transactions for other wallets!")
        transaction_hash = self.calculate_hash().encode()
        self.signature = signing_key.sign(transaction_hash).hex()

    def is_valid(self):
        if self.sender is None:  # Reward transaction
            return True
        if not self.signature:
            raise ValueError("No signature in this transaction")
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1)
        transaction_hash = self.calculate_hash().encode()
        return vk.verify(bytes.fromhex(self.signature), transaction_hash)

    def __str__(self):
        return f'Transaction({self.sender} -> {self.receiver}, Amount: {self.amount}, Signature: {self.signature})'
