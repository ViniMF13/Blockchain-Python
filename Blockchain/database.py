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

def create_transaction_tbl():
    """Cria a tabela de usuários se ela não existir."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaction_tbl (
        sender SERIAL PRIMARY KEY,
        receiver VARCHAR(255) NOT NULL,
        amount FLOAT,
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_transaction(transaction):
    """Insere um novo usuário na tabela."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO transaction_tbl (sender, receiver, amount) VALUES (%s, %s, %s)
    ''', (transaction.sender, transaction.receiver, transaction.amount))
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

def delete_row(table_name, campo, id):
    """Deleta uma linha da tabela."""
    conn = connect_to_db()
    cursor = conn.cursor()

    # Usando psycopg2.sql para evitar injeção de SQL ao inserir o nome da tabela e do campo
    query = sql.SQL('DELETE FROM {table} WHERE {field} = %s').format(
        table=sql.Identifier(table_name),
        field=sql.Identifier(campo)
    )

    try:
        cursor.execute(query, (id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Erro ao deletar a linha: {e}")
    finally:
        cursor.close()
        conn.close()
