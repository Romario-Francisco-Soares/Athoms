from colecoes.colecoes import InsercoesDb
from micro_servicos.json_matrix_engenharia import retornar_json_faces_integracao
import json

novos_rostos = retornar_json_faces_integracao()
json_rostos = json.loads(novos_rostos)
insercoes_db = InsercoesDb()
colRegistro_profissional = insercoes_db.inserir_documento("registro_profissional", json_rostos)
#colRegistro_profissional.insert_many(json_rostos)
#client.list_database_names()
#colection.insert_many(usuario)
#resultados = colection.find()

