import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a URL do banco de dados da variável de ambiente
DATABASE_URL = 'postgresql://postgres:aQQFdueQgyhrdDJSxeUgdxNiipLChEqD@monorail.proxy.rlwy.net:33349/railway'

def connect_to_db():
    """Estabelece uma conexão com o banco de dados."""
    return psycopg2.connect(DATABASE_URL)

def create_table():
    """Cria a tabela de usuários se ela não existir."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        idade INT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_user(nome, email, idade):
    """Insere um novo usuário na tabela."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (nome, email, idade) VALUES (%s, %s, %s)
    ''', (nome, email, idade))
    conn.commit()
    cursor.close()
    conn.close()

def drop_table(table_name):
    """Deleta a tabela."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(sql.SQL('DROP TABLE IF EXISTS {}').format(sql.Identifier(table_name)))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    """Deleta um usuário da tabela."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()