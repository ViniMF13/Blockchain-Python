import re

def le_dados(file_local):
    indice_inteiros = []
    previoushash_list = []
    transaction_number_list = []
    
    try:
        with open(file_local, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        indice = ""
        

        
        for linha in linhas:
            linha = linha.strip()  # Remove espaços em branco no início e fim da linha

            # Le Indice a cada Iteração
            if linha.startswith('i'):
                indice += linha[6:]  # Adiciona caracteres a partir do índice 6 da linha atual
                # Extrai números usando expressão regular
                numeros = re.findall(r'\d+', indice)
                if numeros:
                    indice_int = int(numeros[0])  # Converte o primeiro número encontrado em inteiro
                    indice_inteiros.append(indice_int)  # Adiciona à lista de inteiros
                    indice = ""  # Limpa a string de índices para a próxima linha
            
            # Le Previous Hash a cada Iteração
            if linha.startswith('p'):
                previous_hash = linha[15:]
                previoushash_list.append(previous_hash)


            # Le transactions a cada iteração
            if linha.startswith('t'):
                
                

    except FileNotFoundError:
        print(f"Arquivo '{file_local}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")






    print(f"Índices inteiros encontrados no arquivo '{file_local}':")
    print(indice_inteiros)
    print(previoushash_list)
    # Incluir indices na blockchain

    

# Exemplo de uso:
le_dados('blockchain.txt')
