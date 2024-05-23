# tests/test_blockchain.py
import unittest
from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
import ecdsa

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.sender_private_key = sk
        self.sender_public_key = sk.get_verifying_key().to_string().hex()

    def test_create_transaction(self):
        tx = Transaction(self.sender_public_key, "Bob", 10)
        tx.sign_transaction(self.sender_private_key)
        self.blockchain.create_transaction(tx)
        self.assertEqual(len(self.blockchain.pending_transactions), 1)

    def test_mine_block(self):
        tx = Transaction(self.sender_public_key, "Bob", 10)
        tx.sign_transaction(self.sender_private_key)
        self.blockchain.create_transaction(tx)
        self.blockchain.mine_pending_transactions("miner_address")
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_balance(self):
        tx1 = Transaction(self.sender_public_key, "Bob", 10)
        tx1.sign_transaction(self.sender_private_key)
        self.blockchain.create_transaction(tx1)
        self.blockchain.mine_pending_transactions("miner_address")
        tx2 = Transaction("Bob", self.sender_public_key, 5)
        self.blockchain.create_transaction(tx2)
        self.blockchain.mine_pending_transactions("miner_address")
        self.assertEqual(self.blockchain.get_balance_of_address(self.sender_public_key), 5)
        self.assertEqual(self.blockchain.get_balance_of_address("Bob"), 5)
        self.assertEqual(self.blockchain.get_balance_of_address("miner_address"), 100)

    def test_chain_validity(self):
        tx = Transaction(self.sender_public_key, "Bob", 10)
        tx.sign_transaction(self.sender_private_key)
        self.blockchain.create_transaction(tx)
        self.blockchain.mine_pending_transactions("miner_address")
        self.assertTrue(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()
