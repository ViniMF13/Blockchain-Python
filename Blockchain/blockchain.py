from typing import List, Optional
from .transaction import Transaction
from .block import Block
import time
import os
import json


class Blockchain:
    def __init__(self) -> None:
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty: int = 4
        self.pending_transactions: List[Transaction] = []
        self.mining_reward: int = 50

    def create_genesis_block(self) -> Block:
        return Block(0, "0", [], time.time())
    
    def receive_airdrop(self, address: str) -> None:
        self.pending_transactions.append(Transaction(None, 'Blockchain', address, 1000))

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def get_balance_of_address(self, address: str) -> int:
        balance: int = 0
        # itera pelos blocos da cadeia buscando por todas as transações que envolvem o endereço passado 
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        return balance

    def update_file(self, file_name: str) -> None:
        with open(file_name, 'w') as file:
            json.dump([block.to_json() for block in self.chain], file, indent=4)
        
    def load_from_file(self, file_name: str) -> None:
        if not os.path.exists(file_name):
            return
        # Verifica se o arquivo está vazio
        if os.stat(file_name).st_size == 0:
            return
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                if data:
                    self.chain = [Block.from_json(block_data) for block_data in data]
        except FileNotFoundError:
            pass
