from colecoes.colecoes import registro_profissionais
from micro_servicos.json_matrix_engenharia import retornar_json_faces_integracao
import json

novos_rostos = retornar_json_faces_integracao()
json_rostos = json.loads(novos_rostos)
colRegistro_profissional = registro_profissionais()
colRegistro_profissional.insert_many(json_rostos)

#client.list_database_names()
#colection.insert_many(usuario)
#resultados = colection.find()

