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


    def update_file(self, file_name):
        with open(file_name, 'a') as file:
            file.write(f'======================== Bloco {self.get_latest_block().index} ========================\n')
            file.write(f'index: {self.get_latest_block().index}\n')
            file.write(f'previous_hash: {self.get_latest_block().previous_hash}\n')
            file.write(f'transactions: {len(self.get_latest_block().transactions)}\n')

            for i in range (len(self.get_latest_block().transactions)):
                file.write(f'\tsenderPublicKey: {self.get_latest_block().transactions[i].senderPublicKey}\n')
                file.write(f'\tsender: {self.get_latest_block().transactions[i].sender}\n')
                file.write(f'\treceiver: {self.get_latest_block().transactions[i].receiver}\n')
                file.write(f'\tamount: {self.get_latest_block().transactions[i].amount}\n')
                file.write(f'\tsignature: {self.get_latest_block().transactions[i].signature}\n')
            file.write(f'timestamp: {self.get_latest_block().timestamp}\n')
            