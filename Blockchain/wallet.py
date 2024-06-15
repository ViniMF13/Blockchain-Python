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
            self.__seed_phrase = seed_phrase
            self.__seed = self.mnemonic.to_seed(seed_phrase)
        else:
            self.__seed_phrase = self.mnemonic.generate()
            self.__seed = self.mnemonic.to_seed(self.__seed_phrase)
            print(f'your seed-phras is {self.__seed_phrase} \nThis is the only way to recovery your wallet!!! Keep it safe.')

        self.blockchain = blockchain    
        self.__private_key = self.__generate_private_key()
        self.public_key = self.__generate_public_key(self.__private_key)
        self.address = self.__generate_address(self.public_key)

    def __generate_private_key(self):
        return hashlib.sha256(self.__seed).digest()

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
    
    def receive_airdrop(self):
        for block in self.blockchain.chain:
            for transaction in block.transactions:
                if transaction.sender == self.get_address() or transaction.receiver == self.get_address():
                    print("This address is not eligible for airdrop")
        for transaction in self.blockchain.pending_transactions:
            if transaction.sender == self.get_address() or transaction.receiver == self.get_address():
                print("This address is not eligible for airdrop")
    
        
        self.blockchain.pending_transactions.append(Transaction(None, 'Blockchain', self.get_address(), 1000))
        print("You received 1000 POO")

    def create_transaction(self, receiver, amount):
        if self.blockchain.get_balance_of_address(self.get_address()) < amount:
            print("insuficient ballance")

        transaction = Transaction(self.public_key, self.address, receiver, amount)
        self.sign_transaction(transaction)
        self.blockchain.pending_transactions.append(transaction)
        return transaction

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
    