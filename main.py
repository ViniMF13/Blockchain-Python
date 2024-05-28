from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet

def main():
    # Criação de carteiras
    wallet_A = Wallet()
    wallet_B = Wallet()
    
    print("Carteira A:", wallet_A)
    print("Carteira B:", wallet_B)
    
    # Criação de blockchain
    my_blockchain = Blockchain()
    
    # Criação de transação
    tx1 = Transaction(wallet_A.get_address(), wallet_B.get_address(), 10)
    wallet_A.sign_transaction(tx1)
    
    # Adiciona transação na blockchain
    my_blockchain.create_transaction(tx1)
    
    # Mineração de transações pendentes
    my_blockchain.mine_pending_transactions(wallet_A.get_address())
    
    # Mostrar saldo de carteiras
    print(f"Saldo da carteira A: {my_blockchain.get_balance_of_address(wallet_A.get_address())}")
    print(f"Saldo da carteira B: {my_blockchain.get_balance_of_address(wallet_B.get_address())}")
    
    # Validar blockchain
    print("Blockchain é válida?", my_blockchain.is_chain_valid())

if __name__ == "__main__":
    main()
