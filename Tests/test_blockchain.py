# tests/test_blockchain.py
import unittest
from Blockchain.block import Block
from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain.node import Node
from datetime import datetime

class TestBlock(unittest.TestCase):
    def setUp(self):
        # Código de configuração para inicializar os testes do Block
        self.block = Block(0, [], '0')

    def test_block_creation(self):
        self.assertEqual(self.block.index, 0)
        self.assertEqual(self.block.previous_hash, '0')
        self.assertEqual(self.block.transactions, [])
        self.assertIsInstance(self.block.timestamp, datetime)

    def test_block_hash(self):
        # Testar a geração do hash do bloco
        block_hash = self.block.hash()
        self.assertIsInstance(block_hash, str)
        self.assertEqual(len(block_hash), 64)

    def test_block_to_dict(self):
        # Testar a conversão do bloco para dicionário
        block_dict = self.block.to_dict()
        self.assertIsInstance(block_dict, dict)
        self.assertEqual(block_dict['index'], self.block.index)
        self.assertEqual(block_dict['previous_hash'], self.block.previous_hash)
        self.assertEqual(block_dict['transactions'], self.block.transactions)

    def test_block_from_dict(self):
        # Testar a criação de um bloco a partir de um dicionário
        block_dict = self.block.to_dict()
        new_block = Block.from_dict(block_dict)
        self.assertEqual(new_block.index, self.block.index)
        self.assertEqual(new_block.previous_hash, self.block.previous_hash)
        self.assertEqual(new_block.transactions, self.block.transactions)

    def test_block_nonce(self):
        # Testar o método relacionado ao nonce
        self.block.nonce = 12345
        self.assertEqual(self.block.nonce, 12345)

    def test_block_add_transaction(self):
        # Testar a adição de transações ao bloco
        transaction = Transaction('sender', 'recipient', 100)
        self.block.add_transaction(transaction)
        self.assertIn(transaction, self.block.transactions)

    # Testes adicionais para os métodos de Block

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        # Código de configuração para inicializar os testes do Blockchain
        self.blockchain = Blockchain()

    def test_blockchain_initialization(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)

    def test_add_block(self):
        # Testar a adição de um bloco
        previous_length = len(self.blockchain.chain)
        self.blockchain.add_block([])
        self.assertEqual(len(self.blockchain.chain), previous_length + 1)
        self.assertEqual(self.blockchain.chain[-1].index, previous_length)

    def test_is_chain_valid(self):
        # Testar a validação da cadeia
        self.assertTrue(self.blockchain.is_chain_valid(self.blockchain.chain))

    def test_create_transaction(self):
        # Testar a criação de uma transação
        transaction = self.blockchain.create_transaction('sender', 'recipient', 100)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.sender, 'sender')
        self.assertEqual(transaction.recipient, 'recipient')
        self.assertEqual(transaction.amount, 100)

    def test_add_transaction(self):
        # Testar a adição de uma transação
        transaction = Transaction('sender', 'recipient', 100)
        self.blockchain.add_transaction(transaction)
        self.assertIn(transaction, self.blockchain.pending_transactions)

    def test_mine_pending_transactions(self):
        # Testar a mineração de transações pendentes
        previous_length = len(self.blockchain.chain)
        self.blockchain.mine_pending_transactions('miner_address')
        self.assertEqual(len(self.blockchain.chain), previous_length + 1)
        self.assertEqual(len(self.blockchain.pending_transactions), 0)

    def test_get_balance(self):
        # Testar a obtenção de saldo
        self.blockchain.create_transaction('miner', 'recipient', 100)
        self.blockchain.mine_pending_transactions('miner')
        balance = self.blockchain.get_balance('recipient')
        self.assertEqual(balance, 100)

    def test_save_load_blockchain(self):
        # Testar salvar e carregar a blockchain
        self.blockchain.save_blockchain('test_blockchain.json')
        new_blockchain = Blockchain.load_blockchain('test_blockchain.json')
        self.assertEqual(len(new_blockchain.chain), len(self.blockchain.chain))

    def test_replace_chain(self):
        # Testar a substituição da cadeia
        new_chain = [self.blockchain.chain[0]]
        new_chain.append(Block(1, [], '0'))
        self.blockchain.replace_chain(new_chain)
        self.assertEqual(self.blockchain.chain, new_chain)

    def test_hash_block(self):
        # Testar a função de hash do bloco
        block_hash = self.blockchain.hash_block(self.blockchain.chain[0])
        self.assertIsInstance(block_hash, str)
        self.assertEqual(len(block_hash), 64)

    def test_validate_transaction(self):
        # Testar a validação de uma transação
        transaction = Transaction('sender', 'recipient', 100)
        self.assertTrue(self.blockchain.validate_transaction(transaction))

    # Testes adicionais para os métodos de Blockchain

class TestTransaction(unittest.TestCase):
    def setUp(self):
        # Código de configuração para inicializar os testes do Transaction
        self.transaction = Transaction('sender', 'recipient', 100)

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.sender, 'sender')
        self.assertEqual(self.transaction.recipient, 'recipient')
        self.assertEqual(self.transaction.amount, 100)

    def test_transaction_to_dict(self):
        # Testar a conversão da transação para dicionário
        transaction_dict = self.transaction.to_dict()
        self.assertIsInstance(transaction_dict, dict)
        self.assertEqual(transaction_dict['sender'], 'sender')
        self.assertEqual(transaction_dict['recipient'], 'recipient')
        self.assertEqual(transaction_dict['amount'], 100)

    def test_transaction_from_dict(self):
        # Testar a criação de uma transação a partir de um dicionário
        transaction_dict = self.transaction.to_dict()
        new_transaction = Transaction.from_dict(transaction_dict)
        self.assertEqual(new_transaction.sender, self.transaction.sender)
        self.assertEqual(new_transaction.recipient, self.transaction.recipient)
        self.assertEqual(new_transaction.amount, self.transaction.amount)

    def test_transaction_sign(self):
        # Testar a assinatura de uma transação
        signature = self.transaction.sign('private_key')
        self.assertIsInstance(signature, str)

    def test_transaction_verify(self):
        # Testar a verificação de uma transação
        signature = self.transaction.sign('private_key')
        self.assertTrue(self.transaction.verify(signature))

    # Testes adicionais para os métodos de Transaction

class TestWallet(unittest.TestCase):
    def setUp(self):
        # Código de configuração para inicializar os testes do Wallet
        self.wallet = Wallet()

    def test_wallet_creation(self):
        # Testar a criação da carteira e geração de endereço
        self.assertIsNotNone(self.wallet.address)

    def test_wallet_balance(self):
        # Testar o método de saldo da carteira
        balance = self.wallet.get_balance()
        self.assertIsInstance(balance, int)

    def test_create_transaction(self):
        # Testar a criação de uma transação pela carteira
        transaction = self.wallet.create_transaction('recipient', 100)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.sender, self.wallet.address)
        self.assertEqual(transaction.recipient, 'recipient')
        self.assertEqual(transaction.amount, 100)

    def test_sign_transaction(self):
        # Testar a assinatura de uma transação
        transaction = self.wallet.create_transaction('recipient', 100)
        signature = self.wallet.sign_transaction(transaction)
        self.assertIsInstance(signature, str)

    def test_verify_transaction(self):
        # Testar a verificação de uma transação
        transaction = self.wallet.create_transaction('recipient', 100)
        signature = self.wallet.sign_transaction(transaction)
        self.assertTrue(self.wallet.verify_transaction(transaction, signature))

    def test_generate_keys(self):
        # Testar a geração de chaves
        public_key, private_key = self.wallet.generate_keys()
        self.assertIsInstance(public_key, str)
        self.assertIsInstance(private_key, str)

    def test_load_keys(self):
        # Testar o carregamento de chaves
        public_key, private_key = self.wallet.generate_keys()
        self.wallet.load_keys(public_key, private_key)
        self.assertEqual(self.wallet.public_key, public_key)
        self.assertEqual(self.wallet.private_key, private_key)

    # Testes adicionais para os métodos de Wallet

class TestNode(unittest.TestCase):
    def setUp(self):
        # Código de configuração para inicializar os testes do Node
        self.node = Node()

    def test_node_initialization(self):
        self.assertIsNotNone(self.node)

    def test_register_node(self):
        # Testar o registro de um nó
        self.node.register_node('http://localhost:5000')
        self.assertIn('http://localhost:5000', self.node.nodes)

    def test_resolve_conflicts(self):
        # Testar a resolução de conflitos
        resolved = self.node.resolve_conflicts()
        self.assertIsInstance(resolved, bool)

    def test_sync_chain(self):
        # Testar a sincronização da cadeia
        synced = self.node.sync_chain()
        self.assertIsInstance(synced, bool)

    def test_broadcast_new_block(self):
        # Testar a transmissão de um novo bloco
        new_block = Block(1, [], '0')
        broadcasted = self.node.broadcast_new_block(new_block)
        self.assertTrue(broadcasted)

    def test_get_nodes(self):
        # Testar a obtenção dos nós registrados
        self.node.register_node('http://localhost:5000')
        nodes = self.node.get_nodes()
        self.assertIn('http://localhost:5000', nodes)

    def test_consensus_algorithm(self):
        # Testar o algoritmo de consenso
        self.assertTrue(self.node.consensus_algorithm())

    # Testes adicionais para os métodos de Node

if __name__ == '__main__':
    unittest.main()
