from typing import List, Optional, Union
from .transaction import Transaction
import hashlib
import time
import json

class Block:
    def __init__(
        self,
        index: int,
        previous_hash: str,
        transactions: List[Transaction],
        nonce: int = 0,
        timestamp: Optional[float] = None,
        hash_value: Optional[str] = None
    ) -> None:
        self.index: int = index
        self.previous_hash: str = previous_hash
        self.timestamp: float = timestamp or time.time()
        self.nonce: int = nonce
        self.transactions: List[Transaction] = transactions
        self.hash: str = self.calculate_hash()

    @classmethod
    def from_json(cls, block_data: dict) -> 'Block':
        return cls(
            index=block_data['index'],
            previous_hash=block_data['previous_hash'],
            transactions=[
                Transaction.from_json(tx) for tx in block_data['transactions']
            ],
            nonce=block_data['nonce'],
            timestamp=block_data['timestamp'],
            hash_value=block_data['hash'],
        )    
    
    def to_json(self) -> dict:
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': [tx.to_json() for tx in self.transactions],
            'nonce': self.nonce,
            'hash': self.hash
        }

    def calculate_hash(self) -> str:
        transactions_string = json.dumps([str(tx) for tx in self.transactions], sort_keys=True)
        block_string = f"{self.index}{self.previous_hash}{transactions_string}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __str__(self) -> str:
        return f"Block(index={self.index}, hash={self.hash}, previous_hash={self.previous_hash}, transactions={self.transactions}, nonce={self.nonce})"
