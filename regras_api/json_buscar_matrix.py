from colecoes.colecoes import registro_profissionais

def localizar_cadastros() -> [[object], str]:
    colProf = registro_profissionais()
    lista_cadastros = colProf.find()
    matrix = []
    nomes = []
    for ls in lista_cadastros:
        nomes.append(ls["nm_arquivo"]), matrix.append(ls["matrix"])
    return matrix, nomes

#novos_rostos = retornar_json_faces_integracao()
#json_rostos = json.loads(novos_rostos)
#collection.insert_many(json_rostos)
#client.list_database_names()
#colection.insert_many(usuario)
#resultados = colection.find()
