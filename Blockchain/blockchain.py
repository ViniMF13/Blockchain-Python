# Blockchain/blockchain.py
from .transaction import Transaction
from .block import Block
import time

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 50

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())
    
    def receive_airdrop(self, address):        
        self.pending_transactions.append(Transaction(None, 'Blockchain', address, 1000))

    def get_latest_block(self):
        return self.chain[-1]

    def get_balance_of_address(self, address):
        balance = 0
        #itera pelos blocos da cadeia buscando por todas as transações que envolvem o endereço passado 
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        return balance


    