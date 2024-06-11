from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain import database

def main():
    # Criação da blockchain
    my_blockchain = Blockchain()

    while(1):
        i = my_blockchain.get_latest_block().index
        with open('blockchain.txt', 'a') as file:
            file.write(f'======================== Bloco {i} ========================\n')
            file.write(f'index: {my_blockchain.get_latest_block().index}\n')
            file.write(f'previous_hash: {my_blockchain.get_latest_block().previous_hash}\n')
            file.write(f'transactions: {my_blockchain.get_latest_block().transactions}\n')
            file.write(f'timestamp: {my_blockchain.get_latest_block().timestamp}\n')

        stop = input(' Deseja simular transação?')
        if stop == 'n':
            break

        # Criação de carteiras
        wallet_A = Wallet()
        wallet_B = Wallet()

        print("\nCarteira A:", wallet_A)
        print("Carteira B:", wallet_B)
        
        # Criação de transação
        tx1 = Transaction(wallet_A.get_public_key(), wallet_A.get_address(), wallet_B.get_address(), 10)
        wallet_A.sign_transaction(tx1)
        
        # Adiciona transação na blockchain
        my_blockchain.create_transaction(tx1)
        database.insert_transaction(tx1)
        
        # Mineração de transações pendentes
        my_blockchain.mine_pending_transactions(wallet_A.get_address())
        
        # Mostrar saldo de carteiras
        print(f"Saldo da carteira A: {my_blockchain.get_balance_of_address(wallet_A.get_address())}")
        print(f"Saldo da carteira B: {my_blockchain.get_balance_of_address(wallet_B.get_address())}")
        
        # Validar blockchain
        print("Blockchain é válida?", my_blockchain.is_chain_valid())


if __name__ == "__main__":
    main()
