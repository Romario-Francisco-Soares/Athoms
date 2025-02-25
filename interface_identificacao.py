from metodos_identificacao.matrix_digital_identif import identificador_face
from colecoes.colecoes import registro_profissionais
from regras_api.json_registro_ponto import registrar_ponto

melhor_nome, melhor_id, melhor_matrix = identificador_face()
registro_profissionais = registro_profissionais()
dados_prof_registro = registro_profissionais.find_one({"matrix":melhor_matrix})
print(dados_prof_registro)

registrar_ponto(dados_prof_registro["_id"],
                None,
                dados_prof_registro["matrix_face"],
                dados_prof_registro["matrix_digital"],
                dados_prof_registro["matrix_retina"],
                dados_prof_registro["matrix_senha"],
                None,
                None,
                None
                )