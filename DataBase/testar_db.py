import db


class Usuario:
    def __init__(self, nome, email, idade):
        self.nome = nome
        self.email = email
        self.idade = idade
        self.salvar_no_banco()

    def salvar_no_banco(self):
        """Insere os dados do usuário no banco de dados."""
        db.insert_user(self.nome, self.email, self.idade)

if __name__ == '__main__':

    db.drop_table('users')