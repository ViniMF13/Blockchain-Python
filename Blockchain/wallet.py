from typing import Optional
import hashlib
import ecdsa
from mnemonic import Mnemonic
from .blockchain import Blockchain
from .transaction import Transaction

class Wallet:
    def __init__(self, blockchain: Blockchain = Blockchain, seed_phrase: Optional[str] = None) -> None:
        self.mnemonic: Mnemonic = Mnemonic("english")
        if seed_phrase:
            self.seed_phrase: str = seed_phrase
            self.seed: bytes = self.mnemonic.to_seed(seed_phrase)
        else:
            self.seed_phrase: str = self.mnemonic.generate()
            self.seed: bytes = self.mnemonic.to_seed(self.seed_phrase)

        self.blockchain: Blockchain = blockchain    
        self.__private_key: bytes = self.__generate_private_key()
        self.public_key: bytes = self.__generate_public_key(self.__private_key)
        self.address: str = self.__generate_address(self.public_key)
        

    def __generate_private_key(self) -> bytes:
        return hashlib.sha256(self.seed).digest()

    def __generate_public_key(self, private_key: bytes) -> bytes:
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        return sk.get_verifying_key().to_string()

    def __generate_address(self, public_key: bytes) -> str:
        sha256 = hashlib.sha256(public_key).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256)
        public_key_hash = ripemd160.digest()
        address_hex = '0xbc' + public_key_hash.hex() 
        return address_hex
    
    def sign_transaction(self, transaction: Transaction) -> None:
        sk = ecdsa.SigningKey.from_string(self.__private_key, curve=ecdsa.SECP256k1)
        transaction_hash = transaction.calculate_hash().encode()
        signature = sk.sign(transaction_hash)
        transaction.signature = signature.hex()
    
    
    def get_public_key(self) -> bytes:
        return self.public_key

    def get_address(self) -> str:
        return self.address

    def __str__(self) -> str:
        return f'Address: {self.address}'
    
if __name__ == "__main__":
    wallet = Wallet()

    print("\npublic key:", wallet.get_public_key())

    print("\n",  wallet)
