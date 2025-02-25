from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://romario:Teste1*@cluster0.cvsr2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), ssl=True)
bancoDados = client["ThomasRP"]

def registro_ponto():
    colecao = bancoDados["registro_ponto"]
    return colecao

def registro_profissionais():
    colecao = bancoDados["registro_profissional"]
    return colecao

def definicao_turno():
    colecao = bancoDados["definicao_turno"]
    return colecao

def definicao_sexo():
    colecao = bancoDados["definicao_sexo"]
    return colecao
