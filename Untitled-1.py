def le_dados(file_local, blockchain):
    try:
        with open('blockchain.txt', 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        indice = ""

        i = 0
        for linha in linhas:
    
            linha = linha.strip()  # Remove espaços em branco no início e fim da linha

            if linha.startswith('i'):
                # Verifica se há uma próxima linha
                indice += linhas[i][6:]  # Adiciona caracteres a partir do índice 6 da linha atual
            
            i = i + 1

    except FileNotFoundError:
        print(f"Arquivo {file_local} não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    indice_int = int(''.join(filter(str.isdigit, indice)))
    
    #Atribuir index a blockchain



    

le_dados('blockchain.txt')