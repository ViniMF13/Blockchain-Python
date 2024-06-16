import os
import hashlib
import ecdsa
import base58
from mnemonic import Mnemonic
from .blockchain import Blockchain
from .transaction import Transaction


class Wallet:
    def __init__(self, blockchain=Blockchain, seed_phrase=None):
        self.mnemonic = Mnemonic("english")
        if seed_phrase:
            self.seed_phrase = seed_phrase
            self.seed = self.mnemonic.to_seed(seed_phrase)
        else:
            self.seed_phrase = self.mnemonic.generate()
            self.seed = self.mnemonic.to_seed(self.seed_phrase)
            print(f'your seed-phras: {self.seed_phrase}\n')

        self.blockchain = blockchain    
        self.__private_key = self.__generate_private_key()
        self.public_key = self.__generate_public_key(self.__private_key)
        self.address = self.__generate_address(self.public_key)
        

    def __generate_private_key(self):
        return hashlib.sha256(self.seed).digest()

    def __generate_public_key(self, private_key):
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        return sk.get_verifying_key().to_string()

    def __generate_address(self, public_key) -> str:
        sha256 = hashlib.sha256(public_key).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256)
        public_key_hash = ripemd160.digest()
        address_hex = '0xbc' + public_key_hash.hex() 
        return address_hex
    
    def sign_transaction(self, transaction):
        sk = ecdsa.SigningKey.from_string(self.__private_key, curve=ecdsa.SECP256k1)
        transaction_hash = transaction.calculate_hash().encode()
        signature = sk.sign(transaction_hash)
        transaction.signature = signature.hex()
    
    def verify_seed_phrase(self, input_seed_phrase) -> bool:
        seed = self.mnemonic.to_seed(input_seed_phrase)
        return seed == self.seed 
    
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
    