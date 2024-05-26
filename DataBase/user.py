import db

class User:
    def __init__(self, id, name, password):
        self.__id = id
        self.name = name
        self.__password = password
        self.__balance = 0.0
        self.salvar_no_banco()


#Getter e Setter balance
    def get_balance(self):
        return self.__balance
    
    def set_balance(self, value):
        self.__balance = value
    
#Getter e Setter password    
    def get_password(self):
        return self.__password
    
    def set_password(self, value):
        self.__password = value

#Getter e Setter id
    def get_id(self):
        return self.__id
    
    def set_id(self, value):
        self.__id = value

    def salvar_no_banco(self):
        """Insere os dados do usuário no banco de dados."""
        db.insert_user(self.name, self.__password)

