import json
import base64
import numpy as np
import cv2
from datetime import datetime
from bson.json_util import dumps
from bson import ObjectId  # Importando corretamente o ObjectId
from cryptography.fernet import Fernet
import random
# Libs externas
import face_recognition as fr
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

# Libs internas
from colecoes.colecoes import BuscasDb, InsercoesDb

app = Flask(__name__)
api = Api(app)
CORS(app)  # Permite CORS

class autenticacao(Resource):
    @staticmethod
    def criptografar(string):
        """Criptografa uma string usando a chave especificada."""
        try:
            chave = b'FEX_RTukEVk2ZLHXHO1N5YgayCDEO-UEN4yIAMrp7ug=9JiGe8a332Gse-1j3-cnH8usrla2_a_sdw4'
            cipher_suite = Fernet(chave)
            return cipher_suite.encrypt(string.encode('utf-8')).decode('utf-8')
        except Exception as erro:
            print(f"Erro na função CRIPTOGRAFAR: {erro}")

    @staticmethod
    def descriptografar(string):
        """Descriptografa uma string usando a chave especificada."""
        try:
            chave = b'FEX_RTukEVk2ZLHXHO1N5YgayCDEO-UEN4yIAMrp7ug='
            cipher_suite = Fernet(chave)
            return cipher_suite.decrypt(string.encode('utf-8')).decode('utf-8')
        except Exception as erro:
            print(f"Erro ao descriptografar: {erro}")

    @staticmethod
    def gerar_token():
        lista_ramdomicos = []
        inicial_numero_ram = 1
        final_numero_ram = 999
        letras_busca = 'abcdefghijklmnopqrstuvwxyz'
        k = ''
        for ran in range(32):
            lista_ramdomicos.append(random.randint(inicial_numero_ram, final_numero_ram))
            lista_ramdomicos.append(random.choice(letras_busca))
        for x in lista_ramdomicos:
            k = k + str(x)
        return ''.join(k)

    def post(self):
        try:
            token = None
            data = request.get_json()
            if not data:
                return jsonify({"error": "Usuário ou Senha não informados"}), 400
            busca = BuscasDb()
            resultante = busca.retornar_dados("acesso")
            for res in resultante:
                if data.get('usuario') == res['usuario']:
                    if data.get('senha') == res['senha']:
                        token = self.criptografar(self.gerar_token())
            return {'token': token if token else None}
        except Exception as e:
            return jsonify({"error": str(e)}), 500



def codificar_matrix(string64):
    """Converte uma imagem em base64 para codificação facial."""
    try:
        imagem = string64.split('base64,')[1]
        img_data = base64.b64decode(imagem)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_small_frame = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
        localizacao_do_rosto = fr.face_locations(rgb_small_frame)
        encodings = fr.face_encodings(rgb_small_frame, localizacao_do_rosto)
        return encodings[0].tolist() if encodings else None
    except Exception as e:
        print(f"Erro ao codificar a imagem: {e}")
        return None

class Usuario(Resource):
    @staticmethod
    def convert_objectid(document):
        """Converte ObjectId para string."""
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
        return document

    @staticmethod
    def _parse_date(date_str):
        """Converte string para datetime ISO 8601, retorna None se inválido."""
        try:
            return datetime.fromisoformat(date_str).isoformat() if date_str else None
        except ValueError:
            return None

    def get(self):
        """Recupera usuários com base nos parâmetros passados via query string."""
        try:
            buscas_db = BuscasDb()
            col_prof = json.loads(dumps(buscas_db.retornar_dados('registro_profissional')))
            return jsonify(col_prof)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        """Insere um novo usuário no banco de dados."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dados não fornecidos"}), 400

            matrix_face = codificar_matrix(data.get('matrix_face'))
            if matrix_face is None:
                return jsonify({"error": "Erro ao processar a imagem facial"}), 400

            json_dados = {
                "nm_pessoa_fisica": data.get('nome'),
                "data_nascimento": self._parse_date(data.get('dataNascimento')),
                "ie_sexo": data.get('sexo'),
                "whatsapp": data.get('whatsapp'),
                "email": data.get('email'),
                "estadoCivil": data.get('estadoCivil'),
                "nm_mae": data.get('nm_mae'),
                "whatsapp_mae": data.get('whatsapp_mae'),
                "nm_pai": data.get('nm_pai'),
                "whatsapp_pai": data.get('whatsapp_pai'),
                "cd_pis": data.get('cd_pis'),
                "cd_ctps": data.get('cd_ctps'),
                "cd_eleitor": data.get('cd_eleitor'),
                "cpf": data.get('cd_cpf'),
                "registro_geral": data.get('cd_rg'),
                "ie_qualificacao": data.get('ie_qualificacao'),
                "endereco_natural": data.get('endereco_natural'),
                "endereco_logradouro": data.get('endereco_logradouro'),
                "matrix_face": matrix_face,
                "matrix_digital": data.get('matrix_digi'),
                "matrix_retina": data.get('matrix_retina'),
                "matrix_senha": data.get('matrix_senh'),
                "data_cadastro_original": self._parse_date(data.get('data_cadastro_original')),
                "data_contratacao": self._parse_date(data.get('data_contratacao')),
                "data_ult_alteracao": self._parse_date(data.get('data_ult_alteracao')),
                "nr_seq_prof_ult_alter": data.get('nr_seq_prof_ult_alter'),
                "nr_seq_prof_cadastro": data.get('nr_seq_prof_cadastro'),
                "nr_seq_prof_contratacao": data.get('nr_seq_prof_contratacao')
            }

            insercoes_db = InsercoesDb()
            resultante = insercoes_db.inserir_documento("registro_profissional", json_dados)

            return {'value': resultante}
        except Exception as e:
            return jsonify({"error": str(e)}), 500

class Exibicao(Resource):

    @staticmethod
    def cadastro_profissional():
        try:
            buscas_db = BuscasDb()
            col_prof = json.loads(dumps(buscas_db.retornar_dados('exibicao_cad_prof')))
            return jsonify(col_prof)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get(self):
       try:
           return self.cadastro_profissional()
       except Exception as e:
           print(e)

class HealthCheck(Resource):
    """Recurso para verificação de status da API."""
    def get(self):
        return jsonify({"status": "I'm alive!"})

# Adicionando os recursos na API
api.add_resource(HealthCheck, '/health')
api.add_resource(Usuario, '/usuario')
api.add_resource(Exibicao, '/exibicao')

if __name__ == '__main__':
    app.run(debug=True)
