from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain import database
from Blockchain.node import Node


def main():

    # Criação de blockchain
    my_blockchain = Blockchain()
    my_blockchain.update_file('blockchain.txt')

    wallet_a = Wallet(my_blockchain)
    wallet_b = Wallet(my_blockchain)
    wallet_c = Wallet(my_blockchain)

    while True:
        while True:
            start = input('\nDeseja simular uma transação? ')
            if start == 'n':
                break

            tx1 = wallet_a.create_transaction(wallet_b.get_address(), 10)
            wallet_a.sign_transaction(tx1)

            print(tx1)


            stop = input('\nDeseja simular a mineração? ')
            if stop == 's':
                break


        node1 = Node(my_blockchain)
        node1.mine_pending_transactions(wallet_c.get_address())
        my_blockchain.update_file('blockchain.txt')

        print('Saldo da carteira A: ', my_blockchain.get_balance_of_address(wallet_a.get_address()))
        print('Saldo da carteira B: ',my_blockchain.get_balance_of_address(wallet_b.get_address()))
        print('Saldo da carteira C: ',my_blockchain.get_balance_of_address(wallet_c.get_address()))

        print('Blockchain válida? ', node1.is_chain_valid())
        
        exit = input('Continuar brincando na blockchain? ')
        if exit == 'n': 
            break   

if __name__ == "__main__":
    main()
