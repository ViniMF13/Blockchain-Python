# Blockchain/blockchain.py
from .block import Block
from .transaction import Transaction
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

    def mine_pending_transactions(self, mining_reward_address):
        valid_transactions = [tx for tx in self.pending_transactions if tx.is_valid()]
        block = Block(len(self.chain), self.get_latest_block().hash, valid_transactions)
        block.mine_block(self.difficulty)

        print("Block successfully mined!")
        self.chain.append(block)

        self.pending_transactions = [
            Transaction(None, 'Blockchain', mining_reward_address, self.mining_reward)
        ]

    def create_transaction(self, transaction):
        if not transaction.is_valid():
            raise ValueError("Cannot add invalid transaction to chain")
        self.pending_transactions.append(transaction)

    def get_balance_of_address(self, address):
        balance = 0
        #itera pelos blocos da cadeia buscando por todas as transações que envolvem o endereço passado 
        for block in self.chain:
            for trans in block.transactions:
                if trans.sender == address:
                    balance -= trans.amount
                if trans.receiver == address:
                    balance += trans.amount
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            for transaction in current_block.transactions:
                if not transaction.is_valid():
                    return False
        return True
    
    def atualiza_arquivo(self, file_name):
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
