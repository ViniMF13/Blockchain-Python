from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain.node import Node


def main():

    # Criação de blockchain
    my_blockchain = Blockchain()

    # Criação de carteiras
    wallet_A = Wallet(my_blockchain)
    wallet_B = Wallet(my_blockchain)
    wallet_C = Wallet(my_blockchain)
       
    # Criação e assinatura das transações
    tx1 = wallet_A.create_transaction(wallet_B.get_address(), 100)
    wallet_A.sign_transaction(tx1)

    tx2 = wallet_B.create_transaction(wallet_A.get_address(), 10)
    wallet_B.sign_transaction(tx2)

    
    # Criação do nó e mineração das transações 
    node1 = Node(my_blockchain)
    node1.mine_pending_transactions(wallet_C.get_address())
    
    
    # Mostrar saldo de carteiras
    print(f"Saldo da carteira A: {my_blockchain.get_balance_of_address(wallet_A.get_address())}")
    print(f"Saldo da carteira B: {my_blockchain.get_balance_of_address(wallet_B.get_address())}")
    print(f"Saldo da carteira C: {my_blockchain.get_balance_of_address(wallet_C.get_address())}")
    
    node1.mine_pending_transactions(wallet_C.get_address())
    node1.mine_pending_transactions(wallet_C.get_address())
    print(f"Saldo da carteira C: {my_blockchain.get_balance_of_address(wallet_C.get_address())}")

    # Validar blockchain
    print("Blockchain é válida?", node1.is_chain_valid())

if __name__ == "__main__":
    main()
