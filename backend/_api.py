import face_recognition as fr
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
from datetime import datetime
from flask_cors import CORS
import base64
import numpy as np
import cv2
import matplotlib.pyplot as plt
# Libs internas
from metodos_identificacao.matrix_digital_identif import identificador_face
from colecoes.colecoes import BuscasDb, InsercoesDb

app = Flask(__name__)
api = Api(app)
CORS(app)  # Permite CORS

def converter_base64_imagem(string64):
    imagem = string64.split('base64,')[1]
    img_data = base64.b64decode(imagem)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fr.face_encodings(frame)
    return frame

class Usuario(Resource):
    def get(self):
        try:
            filtro = request.args.get('filtro', type=str)
            projecao = request.args.get('projecao', type=str)
            opcao = request.args.get('opcao', type=str)
            buscas_db = BuscasDb(filtro, projecao, opcao)
            colProf = buscas_db.retornar_dados('registro_profissional')
            return jsonify(colProf)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dados não fornecidos"}), 400

            matrix_face = converter_base64_imagem(data.get('matrix_face'))
            # Convertendo o numpy array para uma lista
            matrix_face_list = matrix_face.tolist()  # Converte para lista para ser serializável

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
                "matrix_face": matrix_face_list,  # Agora matrix_face é uma lista
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
            colRegistro_profissional = insercoes_db.inserir_documento("registro_profissional", json_dados)

            return {'value': colRegistro_profissional}
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def _parse_date(date_str):
        """Converte string para datetime ISO 8601, retorna None se inválido."""
        try:
            return datetime.fromisoformat(date_str).isoformat() if date_str else None
        except ValueError:
            return None


class HealthCheck(Resource):
    def get(self):
        return jsonify({"status": "I'm alive!"})


api.add_resource(HealthCheck, '/health')
api.add_resource(Usuario, '/usuario')

if __name__ == '__main__':
    app.run(debug=True)
