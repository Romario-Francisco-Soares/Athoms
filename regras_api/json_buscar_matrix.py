from colecoes.colecoes import BuscasDb

def localizar_cadastros() -> [[object], str]:
    buscas_db = BuscasDb(filtro=None, projecao=None, opcao=None)  # Exemplo de parâmetros
    colProf = buscas_db.retornar_definicao_sexo()
    lista_cadastros = colProf
    matrix = []
    nomes = []
    for ls in lista_cadastros:
        nomes.append(ls["nm_arquivo"])
        matrix.append(ls["matrix"])
    return matrix, nomes


# Aqui você pode adicionar mais operações se necessário, como manipulação de JSON, etc.
