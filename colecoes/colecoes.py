import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, PyMongoError
from typing import Optional, List

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

uri = "mongodb+srv://romario:Teste1*@cluster0.cvsr2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
database_name = "ThomasRP"

class AcessosBd:
    """Classe para acessar e interagir com o banco de dados MongoDB."""

    def __init__(self):
        self.client = None
        self.db = None
        self.uri = uri
        self.database_name = database_name
        self._connect()

    def _connect(self):
        """Estabelece a conexão com o MongoDB."""
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'), ssl=True)
            self.client.admin.command('ping')  # Testa a conexão
            self.db = self.client[self.database_name]
            logger.info("Conexão bem-sucedida com o MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Erro de conexão com o MongoDB: {e}")
        except PyMongoError as e:
            logger.error(f"Erro ao acessar o banco de dados: {e}")

    def get_collection(self, collection_name: str):
        """Obtém uma coleção específica do banco de dados."""
        try:
            return self.db[collection_name]
        except PyMongoError as e:
            logger.error(f"Erro ao acessar a coleção {collection_name}: {e}")
            return None

    def get_registro_profissionais(self):
        """Retorna a coleção de registros de profissionais."""
        return self.get_collection("registro_profissional")

    def get_registro_ponto(self):
        """Retorna a coleção de registros de ponto."""
        return self.get_collection("registro_ponto")

    def get_definicao_turno(self):
        """Retorna a coleção de definições de turno."""
        return self.get_collection("definicao_turno")

    def get_definicao_sexo(self):
        """Retorna a coleção de definições de sexo."""
        return self.get_collection("definicao_sexo")


class BuscasDb:
    """Classe para buscar dados no banco de dados MongoDB."""

    def __init__(self, filtro: Optional[dict] = None, projecao: Optional[dict] = None, opcao: Optional[List] = None):
        self.acessos_bd = AcessosBd()
        self.filtro = filtro or {}
        self.projecao = projecao or {}
        self.opcao = opcao or []

    def retornar_dados(self, collection_name: str):
        """Método genérico para retornar dados de qualquer coleção."""
        collection = self.acessos_bd.get_collection(collection_name)
        if collection:
            cursor = collection.find(self.filtro, self.projecao)
            if self.opcao:
                cursor = cursor.sort(self.opcao)
            return cursor
        return None


class InsercoesDb:
    """Classe para inserir dados no banco de dados MongoDB."""

    def __init__(self):
        self.acessos_bd = AcessosBd()

    def inserir_documento(self, collection_name: str, classe_dados_documento: dict):
        """Método genérico para inserir documentos em qualquer coleção."""
        if classe_dados_documento:
            collection = self.acessos_bd.get_collection(collection_name)
            if collection:
                try:
                    collection.insert_one(classe_dados_documento)
                    logger.info(f"Documento inserido na coleção {collection_name}: {classe_dados_documento}")
                    return 'Inserção realizada com sucesso'
                except PyMongoError as e:
                    logger.error(f"Erro ao inserir documento na coleção {collection_name}: {e}")
                    return 'Erro na inserção de dados'
        return 'Documento inválido ou coleção inexistente'


def registrar_log(descricao_atividade: str, documento: dict) -> bool:
    """Registra logs de atividades no banco de dados."""
    logger.info(f"{descricao_atividade} {documento}")
    return True


# Exemplo de uso de BuscasDb
#busca = BuscasDb(filtro={"nome": "João"}, projecao={"_id": 0, "nome": 1}, opcao=[("nome", 1)])
#cursor = busca.retornar_dados("registro_profissional")
#for documento in cursor:
#    print(documento)

# Exemplo de uso de InsercoesDb
#insercao = InsercoesDb()
#documento_profissional = {"nome": "João", "idade": 30}
#resultado = insercao.inserir_documento("registro_profissional", documento_profissional)
#print(resultado)