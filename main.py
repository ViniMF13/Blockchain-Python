from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain import database

def main():
    # Criação da blockchain
    my_blockchain = Blockchain()

    # Adiciona bloco genesis ao arquivo txt
    my_blockchain.atualiza_arquivo('blockchain.txt')

    # Criação de carteira
    wallet_A = Wallet()
    wallet_B = Wallet()

    while True:
        start = input('Deseja simular transação?')
        if start == 'n':
            break

        print("\nCarteira A:", wallet_A)
        print("Carteira B:", wallet_B)
        
        # Criação de transação
        tx1 = Transaction(wallet_A.get_public_key(), wallet_A.get_address(), wallet_B.get_address(), 10)
        wallet_A.sign_transaction(tx1)
        
        # Adiciona transação na blockchain
        my_blockchain.create_transaction(tx1)
        
        
    # Mineração de transações pendentes
    my_blockchain.mine_pending_transactions(wallet_A.get_address())
    my_blockchain.atualiza_arquivo('blockchain.txt')

    # Mostrar saldo de carteiras
    print(f"Saldo da carteira A: {my_blockchain.get_balance_of_address(wallet_A.get_address())}")
    print(f"Saldo da carteira B: {my_blockchain.get_balance_of_address(wallet_B.get_address())}")

    # Validar blockchain
    print("\nBlockchain é válida?", my_blockchain.is_chain_valid())

if __name__ == "__main__":
    main()
