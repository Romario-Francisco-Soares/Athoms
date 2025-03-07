from metodos_identificacao.matrix_digital_identif import identificador_face
from colecoes.colecoes import BuscasDb

melhor_nome, melhor_id, melhor_matrix = identificador_face()
buscas_db = BuscasDb({"matrix_face": melhor_matrix})
colProf = buscas_db.retornar_dados('registro_profissional')
for a in colProf:
    print(a)

#from regras_api.json_registro_ponto import registrar_ponto
#registrar_ponto(colProf["_id"],
#                None,
#                colProf["matrix_face"],
#                colProf["matrix_digital"],
#                colProf["matrix_retina"],
#                colProf["matrix_senha"],
#                None,
#                None,
#                None
#                )