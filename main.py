from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain import database
from Blockchain.node import Node


def main():

    Bitcoin = Blockchain()

    walletA = Wallet(Bitcoin)
    walletB = Wallet(Bitcoin, "fitness word east abuse put pet matrix better chalk school doll mule")
    print(walletA)
    print(walletB)

    
    walletA.receive_airdrop()

    nodeA = Node(Bitcoin)
    nodeA.mine_pending_transactions(walletB.get_address())
    
    walletA.create_transaction(walletB.get_address(), 1000)
    walletB.create_transaction(walletA.get_address(), 5)
    
    nodeA.mine_pending_transactions(walletA.get_address())

    print(Bitcoin.get_balance_of_address(walletA.get_address()))
    print(Bitcoin.get_balance_of_address(walletB.get_address()))


if __name__ == "__main__":
    main()
