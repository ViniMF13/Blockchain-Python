import os
import hashlib
import ecdsa

class Wallet:
    def __init__(self):
        self.__private_key = self.__generate_private_key()
        self.public_key = self.__generate_public_key(self.__private_key)
        self.address = self.public_key.hex()

    def __generate_private_key(self):
        return os.urandom(32)

    def __generate_public_key(self, private_key):
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        return sk.get_verifying_key().to_string()


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
    print(wallet)