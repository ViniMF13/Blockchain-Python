import os
import hashlib
import ecdsa
import base58
from .blockchain import Blockchain
from .transaction import Transaction


class Wallet:
    def __init__(self, blockchain = Blockchain) -> None:
        self.blockchain = blockchain
        self.__private_key = self.__generate_private_key()
        self.public_key = self.__generate_public_key(self.__private_key)
        self.address = self.__generate_address(self.public_key)

    def __generate_private_key(self):
        return os.urandom(32)

    def __generate_public_key(self, private_key):
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        return sk.get_verifying_key().to_string()
    

    def __generate_address(self, public_key) -> str:
        sha256 = hashlib.sha256(public_key).digest()
        # RIPEMD-160 hash of the SHA-256 hash
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256)
        public_key_hash = ripemd160.digest()
        # Convert to hexadecimal and add the prefi
        address_hex = '0xbc' + public_key_hash.hex()
        return address_hex

    def create_transaction(self, receiver, amount):
        transaction = Transaction(self.public_key, self.address, receiver, amount, )
        self.sign_transaction(transaction)
        self.blockchain.pending_transactions.append(transaction)
        return transaction
    
    def sign_transaction(self, transaction):
        sk = ecdsa.SigningKey.from_string(self.__private_key, curve=ecdsa.SECP256k1)
        transaction_hash = transaction.calculate_hash().encode()
        signature = sk.sign(transaction_hash)
        transaction.signature = signature.hex()
    
    def get_public_key(self):
        return self.public_key

    def get_address(self):
        return self.address    

    def __str__(self):
        return f'Address: {self.address}'
    
if __name__ == "__main__":
    wallet = Wallet()

    print("\npublic key:", wallet.get_public_key())

    print("\n",  wallet)
    