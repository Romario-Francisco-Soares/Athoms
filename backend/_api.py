import datetime
import json
import base64

import bson
import numpy as np
import cv2
from bson.json_util import dumps
from bson import ObjectId  # Importando corretamente o ObjectId
from cryptography.fernet import Fernet
import random

# Libs externas
import face_recognition as fr
from flask import Flask, request, jsonify, Response, send_from_directory, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from typing import Optional, List

# Libs internas
from colecoes.colecoes import BuscasDb, InsercoesDb
from classes_profissional.dicionarioDados import cadastroPessoa
from metodos_identificacao.matrix_digital_identif import identificador_face
from regras_api.json_buscar_matrix import localizar_cadastros
from regras_api.json_registro_ponto import registrar_ponto

#servidor
from pyngrok import conf, ngrok
from waitress import serve
conf.get_default().auth_token = "2yNDavcGXs6eKL4yQUWGTTbkxKM_4ga1V1KPGT4YvtpHBhwCU"
NGROK_DOMAIN = "grackle-skilled-usually.ngrok-free.app"

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)  # Permite CORS

lista_consultados_front = []
rostos_conhecidos, nomes_dos_rostos, _id = [],[],[]
matrix_conhecidas = []
profissionais = []
acessos = []
perfis = []

def localizar_matrix_tipo(inf):
    count = 0
    if inf.get('matrix_face'):
        count = 1
        if inf.get('matrix_senha'):
            count += 1
        if inf.get('matrix_digital'):
            count += 1
        if inf.get('matrix_retina'):
            count += 1
    if count > 1:
        print('Contador maior que 1, há algo estranho no trafego')
        return None, None, None, None

    if inf.get('matrix_face'):
        matrix_face = codificar_matrix('f', inf.get('matrix_face'))
        us_name, id_usuario, matrix = reconhecer_matrix('f', matrix_face)
        return us_name, id_usuario, matrix, 'face'
    elif inf.get('matrix_digital'):
        us_name, id_usuario, matrix = reconhecer_matrix('d', inf.get('matrix_digital'))
        return us_name, id_usuario, matrix, 'digital'
    elif inf.get('matrix_retina'):
        us_name, id_usuario, matrix = reconhecer_matrix('r', inf.get('matrix_retina'))
        return us_name, id_usuario, matrix, 'retina'
    elif inf.get('matrix_senha'):
        us_name, id_usuario, matrix = reconhecer_matrix('s', inf.get('matrix_senha'))
        return us_name, id_usuario, matrix, 'senha'

    return None, None, None, None

def carregar_matrix():
    projecao = {"nm_pessoa_fisica": 1, "matrix_senha": 1, "_id": 1}
    busca = BuscasDb(projecao=projecao)
    ls = list(busca.retornar_dados("registro_profissional"))
    if not ls:
        return []
    if ls:
        return ls

def carregar_acesso():
    projecao = {"usuario": 1,
               "senha": 1,
               "nr_seq_profissional": 1,
               "nr_seq_empresa": 1,
               "nr_seq_perfil": 1,
               "_id": 1}
    busca = BuscasDb(projecao=projecao)
    ls = list(busca.retornar_dados("acesso"))
    if not ls:
        return []
    if ls:
        return ls

def carregar_profissional():
    buscas_db = BuscasDb()
    ls = list(buscas_db.retornar_dados('registro_profissional'))
    print('profissionais', ls)
    if not ls:
        return []
    if ls:
        return ls

def carregar_perfis():
    projecao = {"_id":1,
                "nm_perfil":1,
                "consulta_profissional":1,
                "consulta_ponto":1,
                "consulta_servicos":1,
                "cadastro_turnos":1,
                "cadastro_profissionais":1,
                "registrar":1,
                "configuracoes":1,
                "nr_seq_empresa":1}
    busca = BuscasDb(projecao=projecao)
    ls = list(busca.retornar_dados("perfil"))
    if not ls:
        return []
    if ls:
        return ls

def reconhecer_matrix(tipo, matrix):
    try:
        global matrix_conhecidas, rostos_conhecidos, nomes_dos_rostos, _id
        if tipo == 's':
            for n in matrix_conhecidas:
                s = descriptografar(n["matrix_senha"]) if n["matrix_senha"] else ''
                if s == matrix:
                    return n["nm_pessoa_fisica"], n["_id"], n["matrix_senha"]
        if tipo == 'f':
            return identificador_face(matrix, rostos_conhecidos, nomes_dos_rostos, _id)
        if tipo == 'd':
            return None, None, None
        if tipo == 'r':
            return None, None, None

        return None, None, None

    except Exception as e:
        print(e)

def criptografar(string):
    """Criptografa uma string usando a chave especificada."""
    try:
        chave = b'FEX_RTukEVk2ZLHXHO1N5YgayCDEO-UEN4yIAMrp7ug='
        cipher_suite = Fernet(chave)
        return cipher_suite.encrypt(string.encode('utf-8')).decode('utf-8')
    except Exception as erro:
        print(f"Erro na função CRIPTOGRAFAR: {erro}")

def descriptografar(string):
    """Descriptografa uma string usando a chave especificada."""
    try:
        if not string:
            return None
        chave = b'FEX_RTukEVk2ZLHXHO1N5YgayCDEO-UEN4yIAMrp7ug='
        cipher_suite = Fernet(chave)
        return cipher_suite.decrypt(string.encode('utf-8')).decode('utf-8')
    except Exception as erro:
        print(f"Erro ao descriptografar: {erro}")
from flask import request, jsonify, Response
from flask_restful import Resource
import datetime

class Autenticacao(Resource):
    def post(self):
        try:
            data = request.get_json()
            token = ''
            if not data.get("login") or not data.get("password"):
                return {"error": "Usuário ou senha não informados"}, 400

            for prof in acessos:
                if data.get('login') == prof["usuario"]:
                    senha_descriptografada = descriptografar(prof['senha'])
                    if data.get('password') == senha_descriptografada:
                        for p in perfis:
                            if p["_id"] == prof["nr_seq_perfil"] and p["nr_seq_empresa"] == prof["nr_seq_empresa"]:
                                token = criptografar(dumps({
                                    "nr_seq_profissional": prof["nr_seq_profissional"],
                                    "nr_seq_empresa": prof["nr_seq_empresa"],
                                    "nr_seq_perfil": prof["nr_seq_perfil"],
                                    "dt_acesso": datetime.datetime.now().isoformat(),
                                    "dado_perfil": p
                                }))
                                break
                        response = Response(
                            response=jsonify({"message": "Login realizado com sucesso"}).get_data(as_text=True),
                            status=200,
                            mimetype="application/json"
                        )
                        response.set_cookie(
                            "auth_token",
                            token,
                            httponly=True,
                            secure=True,
                            #samesite="Lax",
                            samesite=None,
                            max_age=3600
                        )
                        return response

            return {"error": "Credenciais inválidas"}, 400

        except Exception as e:
            return {"error": str(e)}, 500



def codificar_matrix(tipo, string64):
    """Converte uma imagem em base64 para codificação facial."""
    try:
        if tipo == 'f':
            imagem = string64.split('base64,')[1]
            img_data = base64.b64decode(imagem)
            nparr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            rgb_small_frame = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
            localizacao_do_rosto = fr.face_locations(rgb_small_frame)
            encodings = fr.face_encodings(rgb_small_frame, localizacao_do_rosto)
            return encodings[0].tolist() if encodings else None
        if tipo == 's':
            return criptografar(string64)
    except Exception as e:
        print(f"Erro ao codificar a imagem: {e}")
        return None, None, None

class Usuario(Resource):
    @staticmethod
    def convert_types(document):
        """Converte campos ObjectId e datetime para string ou ISO format."""
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, datetime.datetime):
                document[key] = value.isoformat()
            elif isinstance(value, list):
                document[key] = [Usuario.convert_types(v) if isinstance(v, dict) else v for v in value]
            elif isinstance(value, dict):
                document[key] = Usuario.convert_types(value)
        return document

    def get(self):
        try:
            global profissionais
            auth = request.cookies.get("auth_token")
            dados_profissional = json.loads(descriptografar(auth))
            profs = []
            for prof in profissionais:
                if prof.get("nr_seq_empresa") and str(prof["nr_seq_empresa"]) == dados_profissional["nr_seq_empresa"]["$oid"]:
                    prof_convertido = Usuario.convert_types(prof.copy())
                    profs.append(prof_convertido)
            return jsonify(profs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dados não fornecidos"}), 400

            matrix_face = codificar_matrix('f', data.get('matrix_face'))
            if matrix_face is None:
                return jsonify({"error": "Erro ao processar a imagem facial"}), 400
            else:
                json_dados = cadastroPessoa(data, matrix_face)
                insercoes_db = InsercoesDb()
                resultante = insercoes_db.inserir_documento("registro_profissional", json_dados)
                return {'value': resultante}
        except Exception as e:
            return jsonify({"error": str(e)}), 500

class Exibicao(Resource):
    @staticmethod
    def cadastro_profissional():
        try:
            filtro= {}
            projecao= {}
            opcao = []
            buscas_db = BuscasDb(filtro, projecao, opcao)
            col_prof = json.loads(dumps(buscas_db.retornar_dados('exibicao_cad_prof')))
            print(col_prof)
            print('lista',list(buscas_db.retornar_dados('exibicao_cad_prof')))
            return jsonify(col_prof)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get(self):
        try:
            data = request.get_json()
            print('exibicao', data)
            #data.get('filtro'), data.get('projecao'), data.get('opcao')
            return self.cadastro_profissional()
        except Exception as e:
            print(e)

class Animacoes(Resource):
    @staticmethod
    def ler_json_gif(diretorio_gif):
        try:
            with open(diretorio_gif, 'r', encoding='utf-8') as arquivo:
                arq_json = json.load(arquivo)
                return arq_json
        except Exception as e:
            print(f"Erro ao ler o arquivo JSON do GIF: {e}")
            return None

    dir_gif = './static/'

    def get(self, filename):
        try:
            if not filename.endswith('.json'):
                return jsonify({"error": "Falha ao carregar o arquivo de animação"}), 500
            gif_data = self.ler_json_gif(self.dir_gif+filename)
            if not gif_data:
                return jsonify({"error": "Falha ao carregar o arquivo de animação"}), 500
            return jsonify({"gif": gif_data})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


class Registro(Resource):

    global lista_consultados_front

    def post(self):
        data = request.get_json()
        self.us_name,self.id_usuario,self.matrix,self.tipo = '', '', '', ''
        for x in lista_consultados_front:
            if x["chave_registro"] == data["chave_registro"]:
                self.us_name = x["dados_registro"]['nome']
                self.id_usuario = x["dados_registro"]['id_usuario']
                self.matrix = x["dados_registro"]['matrix']
                self.tipo = x["dados_registro"]['tipo']
        if not self.id_usuario or not self.matrix or not self.tipo:
            return jsonify({"status": 400, "erro": "Não foi possível registrar, tente novamente."})
        rgp = registrar_ponto(
            str(self.id_usuario),
            self.matrix if self.tipo == 'face' else '',
            self.matrix if self.tipo == 'digital' else '',
            self.matrix if self.tipo == 'retina' else '',
            self.matrix if self.tipo == 'senha' else '',
            str(self.id_usuario)
        )
        return jsonify({"status": 200, "status_registro": 200}) if rgp else jsonify({"status": 400, "erro": "Registro de ponto não realizado, horário fora da escala de trabalho"})

class Reconhecimento(Resource):

    global lista_consultados_front
    def post(self):
        data = request.get_json()
        self.us_name, self.id_usuario, self.matrix, self.tipo = localizar_matrix_tipo(data)
        self.chave_registro = Fernet.generate_key()
        if not self.id_usuario or not self.matrix or not self.tipo:
            return jsonify({"status": 400, "erro": "Posicione corretamente seu rosto."})
        lista_consultados_front.append({"chave_registro": self.chave_registro.decode(),
                                  "dados_registro":{
                                      "nome": self.us_name,
                                      "id_usuario": self.id_usuario,
                                      "matrix": self.matrix,
                                      "tipo": self.tipo}
                                })
        return jsonify({"status": 200, "status_registro": 400, "nome": self.us_name, "chave_registro": self.chave_registro.decode()})

from flask import request
from flask_restful import Resource
import datetime

class Acessos(Resource):
    def get(self):
        try:
            # 1. Lê o token do cookie
            token = request.cookies.get("auth_token")
            if not token:
                return {"error": "Token não encontrado"}, 401
            try:
                dados = json.loads(descriptografar(token))
            except Exception as e:
                print(e)
                return {"error": "Token inválido"}, 401
            # 3. Valida data de acesso ou expiração (se for o caso)
            data_acesso = datetime.datetime.fromisoformat(dados["dt_acesso"])
            if (datetime.datetime.now() - data_acesso).seconds > 3600:
                return {"error": "Token expirado"}, 401
            # 4. Continua com acesso autorizado
            response = {"dados_perfil": {"nm_perfil":dados["dado_perfil"]['nm_perfil'],
                                     "consulta_profissional": dados["dado_perfil"]['consulta_profissional'],
                                     "consulta_ponto": dados["dado_perfil"]['consulta_ponto'],
                                     "consulta_servicos": dados["dado_perfil"]['consulta_servicos'],
                                     "cadastro_turnos": dados["dado_perfil"]['cadastro_turnos'],
                                     "cadastro_profissionais": dados["dado_perfil"]['cadastro_profissionais'],
                                     "registrar": dados["dado_perfil"]['registrar'],
                                     "configuracoes": dados["dado_perfil"]['configuracoes'],
                                     "nr_seq_empresa": dados["dado_perfil"]['nr_seq_empresa']}}, 200
            return response
        except Exception as e:
            print('except final', e)
            return {"error": str(e)}, 500

class Home(Resource):
    def get(self):
        return send_from_directory('./static/dist', 'index.html')

class Assets(Resource):
    def get(self, filename):
        return send_from_directory('./static/dist/assets', filename)

# Adicionando os recursos na API
api.add_resource(Usuario, '/usuario')
api.add_resource(Acessos, '/listar_acessos')
api.add_resource(Autenticacao, '/login')
api.add_resource(Exibicao, '/exibicao')
api.add_resource(Registro, '/registro_ponto')
api.add_resource(Reconhecimento, '/reconhecer_credenciais')

# Adicionando os recursos do Front'end
api.add_resource(Home,'/')
api.add_resource(Assets,'/assets/<string:filename>')
api.add_resource(Animacoes, '/gifs/<string:filename>')

if __name__ == '__main__':
    #import dlib print(dlib.DLIB_USE_CUDA, 'Para processamento GPU')
    rostos_conhecidos, nomes_dos_rostos, _id = localizar_cadastros()
    matrix_conhecidas = carregar_matrix()
    acessos = carregar_acesso()
    profissionais = carregar_profissional()
    perfis = carregar_perfis()
    #app.run(debug=True)

    serve(app, host="127.0.0.1", port=5000)
    tunnel = ngrok.connect(5000, domain=NGROK_DOMAIN, threads=10)

    # Tem que rodar no cmd para o servidor ngrok executar:
    # site ngrok: https://dashboard.ngrok.com/get-started/setup/python
    # Conta: google
    # instalar NGrok: python -m pip install ngrok
    # Acessar diretório: C:\Users\ux33826\AppData\Local\ngr ok
    # criar arquivo: ngrok.yml

    # Escrever dentro do arquivo: (quebrar por linha)
    # region: us
    # version: '2'
    # authtoken: 2yNDavcGXs6eKL4yQUWGTTbkxKM_4ga1V1KPGT4YvtpHBhwCU

    #Após a escrita do arquivo, abra o cmd e execute:
    #Ativar o túnel:  ngrok http --domain=grackle-skilled-usually.ngrok-free.app 5000

    # Após todos os passos, o site será publicado em:
    # https://grackle-skilled-usually.ngrok-free.app/
