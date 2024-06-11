from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain import database

def main():
    i = 0

    # Criação de blockchain
    my_blockchain = Blockchain()
    with open('blockchain.txt', 'a') as file:
        file.write(f'======================== Bloco {i} ========================\n')
        file.write(f'index: {my_blockchain.get_latest_block().index}\nprevious_hash: {my_blockchain.get_latest_block().previous_hash}\ntransactions: {my_blockchain.get_latest_block().transactions}\ntimestamp: {my_blockchain.get_latest_block().timestamp}\n')

    
    while(1):
        i = i + 1
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

        ####################### ADICIONAR AO ARQUIVO TXT ############################################

        with open('blockchain.txt', 'a') as file:
            file.write(f'======================== Bloco {i} ========================\n')
            file.write(f'index: {my_blockchain.get_latest_block().index}\nprevious_hash: {my_blockchain.get_latest_block().previous_hash}\ntransactions: {my_blockchain.get_latest_block().transactions}\ntimestamp: {my_blockchain.get_latest_block().timestamp}\n')

        print('\n')
        stop = input('DESEJA PARAR?')
        if stop == 's': 
            break


if __name__ == "__main__":
    main()
