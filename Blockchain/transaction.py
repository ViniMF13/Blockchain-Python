import hashlib
import ecdsa
import _json

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def calculate_hash(self):
        transaction_string = f"{self.sender}{self.receiver}{self.amount}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def sign_transaction(self, private_key):
        if not self.sender or not self.receiver:
            raise ValueError("Transaction must include sender and receiver")
        
        if private_key.to_string().hex() != self.sender:
            raise ValueError("You cannot sign transactions for other wallets")

        hash_tx = self.calculate_hash()
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key.to_string().hex()), curve=ecdsa.SECP256k1)
        self.signature = sk.sign(hash_tx.encode()).hex()

    def is_valid(self):
        if self.sender is None:  # Mining reward transaction
            return True
        if self.signature is None:
            raise ValueError("No signature in this transaction")
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1)
        try:
            return vk.verify(bytes.fromhex(self.signature), self.calculate_hash().encode())
        except ecdsa.BadSignatureError:
            return False

    def __str__(self):
        return f"Transaction(sender={self.sender}, receiver={self.receiver}, amount={self.amount}, signature={self.signature})"
