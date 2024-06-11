import hashlib
import json
import ecdsa

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
    
    def verify_transaction(self):
        # Recalcula o endereço a partir da chave pública
        sha256 = hashlib.sha256(self.senderPublicKey).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256)
        public_key_hash = ripemd160.digest()
        recalculated_address = '0xbc' + public_key_hash.hex()
        
        # Compara o endereço recalculado com o endereço na transação
        if recalculated_address != self.sender:
            raise "recalculated_address is diffrent than sender address"
        # Verifica a assinatura
        vk = ecdsa.VerifyingKey.from_string(self.senderPublicKey, curve=ecdsa.SECP256k1)
        transaction_hash = self.calculate_hash().encode()
        try:
            vk.verify(bytes.fromhex(self.signature), transaction_hash)
            return True 
        except ecdsa.BadSignatureError:
            print("falha ao verificar transação")
            return False

    def is_valid(self):
        if self.sender == 'Blockchain' :  # Reward transaction
            return True
        if not self.signature:
            raise ValueError("No signature in this transaction")
        
        return self.verify_transaction()
    

    def __str__(self):
        return f'Transaction({self.sender} -> {self.receiver}, Amount: {self.amount}, Signature: {self.signature})'