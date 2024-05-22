# main.py
from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction

def main():
    # Cria a blockchain
    coin = Blockchain()

    # Cria algumas transações
    coin.create_transaction(Transaction("Alice", "Bob", 10))
    coin.create_transaction(Transaction("Bob", "Alice", 5))

    # Minera os blocos
    print("Mining block 1...")
    coin.mine_pending_transactions("miner_address")

    print("Balance of miner: ", coin.get_balance_of_address("miner_address"))

    print("Mining block 2...")
    coin.mine_pending_transactions("miner_address")

    print("Balance of miner: ", coin.get_balance_of_address("miner_address"))

    # Valida a blockchain
    print("Is blockchain valid?", coin.is_chain_valid())

if __name__ == "__main__":
    main()
