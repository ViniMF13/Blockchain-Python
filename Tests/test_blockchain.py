# tests/test_blockchain.py
import unittest
from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def test_create_transaction(self):
        self.blockchain.create_transaction(Transaction("Alice", "Bob", 10))
        self.assertEqual(len(self.blockchain.pending_transactions), 1)

    def test_mine_block(self):
        self.blockchain.create_transaction(Transaction("Alice", "Bob", 10))
        self.blockchain.mine_pending_transactions("miner_address")
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_balance(self):
        self.blockchain.create_transaction(Transaction("Alice", "Bob", 10))
        self.blockchain.mine_pending_transactions("miner_address")
        self.blockchain.create_transaction(Transaction("Bob", "Alice", 5))
        self.blockchain.mine_pending_transactions("miner_address")
        self.assertEqual(self.blockchain.get_balance_of_address("Alice"), 5)
        self.assertEqual(self.blockchain.get_balance_of_address("Bob"), 5)
        self.assertEqual(self.blockchain.get_balance_of_address("miner_address"), 100)

    def test_chain_validity(self):
        self.blockchain.create_transaction(Transaction("Alice", "Bob", 10))
        self.blockchain.mine_pending_transactions("miner_address")
        self.assertTrue(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()
