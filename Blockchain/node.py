from .transaction import Transaction
from .blockchain import Blockchain
from .block import Block
import hashlib
import ecdsa
from typing import Optional, Union, List

class Node:
    def __init__(self, blockchain: Blockchain) -> None:
        self.blockchain: Blockchain = blockchain

    def verify_transaction(self, transaction: Transaction) -> bool:
        # Verifica se é uma recompensa de mineração
        if transaction.sender == 'Blockchain':
            return True
        # Recalcula o endereço a partir da chave pública
        sha256 = hashlib.sha256(transaction.senderPublicKey).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256)
        public_key_hash = ripemd160.digest()
        recalculated_address = '0xbc' + public_key_hash.hex()
        
        # Compara o endereço recalculado com o endereço na transação
        if recalculated_address != transaction.sender:
            raise ValueError("recalculated_address is different than sender address")
        # Verifica a assinatura
        vk = ecdsa.VerifyingKey.from_string(transaction.senderPublicKey, curve=ecdsa.SECP256k1)
        transaction_hash = transaction.calculate_hash().encode()
        try:
            vk.verify(bytes.fromhex(transaction.signature), transaction_hash)
            return True 
        except ecdsa.BadSignatureError:
            print("falha ao verificar transação")
            return False

    def is_valid(self, transaction: Transaction) -> bool:
        if transaction.sender == 'Blockchain':  # Reward transaction
            return True
        if not transaction.signature:
            raise ValueError("No signature in this transaction")
        return self.verify_transaction(transaction)        
    
    def mine_pending_transactions(self, mining_reward_address: str) -> None:
        valid_transactions: List[Transaction] = [tx for tx in self.blockchain.pending_transactions if self.is_valid(tx)]
        valid_transactions.append(Transaction(None, 'Blockchain', mining_reward_address, self.blockchain.mining_reward))
        block: Block = Block(len(self.blockchain.chain), self.blockchain.get_latest_block().hash, valid_transactions)
        block.mine_block(self.blockchain.difficulty)

        self.blockchain.chain.append(block)
        self.blockchain.pending_transactions = []

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.blockchain.chain)):
            current_block: Block = self.blockchain.chain[i]
            previous_block: Block = self.blockchain.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            for transaction in current_block.transactions:
                if not self.verify_transaction(transaction):
                    return False
        return True
