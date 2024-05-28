from Blockchain.blockchain import Blockchain
from Blockchain.transaction import Transaction
from Blockchain.wallet import Wallet
from Blockchain import database
import user


def main():
    # Criação de carteiras

    #email = input('Digite o email:')
    #senha = input('Digite a senha: ')
    email = 'newuser@example.com'
    senha = 'new_password'
    logged = database.login_user(email, senha)

    while logged == False:
        print('\nCredenciais incorretas\ntente novamente.')
        email = input('Digite o email:')
        senha = input('Digite a senha: ')
        logged = database.login_user(email, senha)

    usuario = user.User(email, senha, 'nome_consultado')    
    
    wallet_A = usuario.wallet
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