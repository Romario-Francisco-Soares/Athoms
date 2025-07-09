from metodos_identificacao.matrix_digital_identif import identificador_face
from colecoes.colecoes import BuscasDb

melhor_nome, melhor_id, melhor_matrix = identificador_face()
buscas_db = BuscasDb({"matrix_face": melhor_matrix})
colProf = buscas_db.retornar_dados('registro_profissional')
for a in colProf:
    print(a)

