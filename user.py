from Blockchain.wallet import Wallet
from Blockchain import database
import bcrypt

class User:
    def __init__(self, email, senha, nome):
        self.email = email
        self.__senha = self.hash_senha(senha)  # Armazenando o hash da senha como string decodificada
        self.nome = nome
        self.wallet = Wallet()

    def hash_senha(self, senha):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')  # Decodificando para string

    def get_senha(self):
        return self.__senha

    def verify_senha(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.__senha.encode('utf-8'))  # Codificando de volta para bytes
    




