import json
import base64
import logging

import numpy as np
import cv2
from bson.errors import InvalidId
from bson.json_util import dumps
from bson import ObjectId
from cryptography.fernet import Fernet

# Libs externas
import face_recognition as fr
from flask import Flask, request, jsonify, Response, send_from_directory, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from typing import Optional, List

# Libs internas
from colecoes.colecoes import BuscasDb, InsercoesDb
from classes_profissional.dicionarioDados import cadastroPessoa
from classes_profissional.classesDados import class_turno

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
CORS(app, supports_credentials=True)

lista_consultados_front = []
rostos_conhecidos, nomes_dos_rostos, _id = [],[],[]
matrix_conhecidas = []
profissionais = []
acessos = []
perfis = []

def simplificar_oid(obj):
    if isinstance(obj, dict):
        # Se for um dict com apenas "$oid", retorna o valor direto
        if set(obj.keys()) == {"$oid"}:
            return obj["$oid"]
        # Caso contrário, percorre recursivamente
        return {k: simplificar_oid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [simplificar_oid(item) for item in obj]
    else:
        return obj

def retornar_dados_autenticacao(token_encriptado, ds_requisitado):
    try:
        token_descriptografado = json.loads(descriptografar(token_encriptado))
        token_descriptografado_tratado = simplificar_oid(token_descriptografado)
        ls_opcoes = ["nr_seq_profissional", "nr_seq_empresa", "nr_seq_perfil", "dt_acesso", "dado_perfil"]
        ls_sub_opcoes = ["_id","nm_perfil","cadastro_profissionais","cadastro_turnos","configuracoes",
                         "nr_seq_empresa","consulta_ponto","consulta_profissional",
                         "consulta_servicos","registrar","consulta_turnos"]
        if ds_requisitado in ls_opcoes:
            return token_descriptografado_tratado[ds_requisitado]
        elif ds_requisitado in ls_sub_opcoes:
            return token_descriptografado_tratado["dado_perfil"][ds_requisitado]
        else:
            return None
    except Exception as e:
        logging.error(f"erro ao obter dados do token: {e}")
        return None


def mes_para_numero(nome_mes: str):
    """
    Converte o nome de um mês (em português ou inglês, completo ou abreviado) para seu número (1-12).
    Retorna None se o mês não for reconhecido.
    """
    nome_mes = nome_mes.strip().lower()
    # Dicionário personalizado para meses em português
    meses_pt = {'janeiro': 1,'fevereiro': 2,
        'março': 3,'abril': 4,'maio': 5,'junho': 6,
        'julho': 7,'agosto': 8,'setembro': 9,'outubro': 10,'novembro': 11,'dezembro': 12,
    }
    if nome_mes in meses_pt:
        return meses_pt[nome_mes]
    return None

def cadastrar_turno(data, nr_seq_empresa):
    def gera_data_isoformat(hr_para_formatar: str):
        from datetime import datetime
        data_fixa = "2025-01-01"
        dt = datetime.fromisoformat(f"{data_fixa}T{hr_para_formatar}")
        return dt.isoformat()
    try:
        prevchegada = data["prevchegada"]
        prevsaidaalm = data["prevsaidaalm"]
        prevreturnoalm = data["prevreturnoalm"]
        prevsaida = data["prevsaida"]

        turno = class_turno(
            data["turno"],
            data["anovalidade"],
            mes_para_numero(data["mesvalidade"]),
            data["semanavalidade"] if data["semanavalidade"] != 'Todas' else 6,
            data["diasemana"] if data["diasemana"] != 'Todos os dias' else 8,
            gera_data_isoformat(prevchegada),
            gera_data_isoformat(prevsaidaalm),
            gera_data_isoformat(prevreturnoalm),
            gera_data_isoformat(prevsaida),
            data["intervaloalmoco"],
            data["registroantecedencia"],
            data["registroatraso"],
        nr_seq_empresa).criar_json_escala()
        resultante = InsercoesDb().inserir_documento('definicao_turno', turno)
        if not resultante:
            return {'error': 'Erro no cadastro'}, 400
        return {'return_post': 'Cadastro realizado com sucesso!'}, 200

    except Exception as e:
        return {"error": str(e)}, 500


def atualizar_turno(data):
    try:
        filtro = {"_id": ObjectId(str(data[1]['_id']).strip())}
    except (InvalidId, TypeError) as e:
        logging.error({"error": f"_id inválido: {e}"})
        return {"error": f"_id inválido: {e}"}, 400
    try:
        db = InsercoesDb()
        documento_em_string = Turnos.convert_types(data[0].copy())
        documento_em_string.pop("_id", None)  # remove _id antes
        documento_com_objectid = converter_campos_para_objectid(documento_em_string, ['_id', 'nr_seq_empresa'])
        sucesso = db.atualizar_documento("definicao_turno", filtro, documento_com_objectid)
        if sucesso:
            logging.info(sucesso)
            return {"return_post": "Atualização realizada com sucesso"}, 200
        else:
            return {"error": "Erro ao atualizar o documento"}, 500
    except Exception as e:
        logging.error(f'Erro ao atualizar turno: {e}')




def atualizar_pessoa(data):

    try:
        filtro = {"_id": ObjectId(str(data[1]['_id']).strip())}
        db = InsercoesDb()
        documento_em_string = Turnos.convert_types(data[0].copy())
        documento_em_string.pop("_id", None)  # remove _id antes
        documento_com_objectid = converter_campos_para_objectid(documento_em_string,
                                                                ['_id', 'nr_seq_empresa', 'nr_seq_prof_ult_alter',
                                                                 'nr_seq_prof_cadastro', 'nr_seq_prof_contratacao'])
        sucesso = db.atualizar_documento("registro_profissional", filtro, documento_com_objectid)
        if sucesso:
            logging.info(sucesso)
            return {"return_post": "Atualização realizada com sucesso"}, 200
        else:
            return {"error": "Erro ao atualizar o documento"}, 500

    except (InvalidId, TypeError) as e:
        logging.error({"error": f"_id inválido: {e}"})
        return {"error": f"_id inválido: {e}"}, 400


def converter_campos_para_objectid(documento: dict, campos_oid: list) -> dict:
    def _converter(item):
        if isinstance(item, dict):
            for campo in campos_oid:
                valor = item.get(campo)
                if isinstance(valor, str):
                    try:
                        item[campo] = ObjectId(valor)
                    except (InvalidId, TypeError):
                        item[campo] = None
            # Recursão para dicionários dentro do dicionário
            for chave, valor in item.items():
                if isinstance(valor, dict):
                    item[chave] = _converter(valor)
                elif isinstance(valor, list):
                    item[chave] = [_converter(subitem) for subitem in valor]
        return item

    return _converter(documento.copy())

def cadastrar_pessoa(data):
    try:
        matrix_face = codificar_matrix('f', data.get('matrix_face'))
        if matrix_face is None:
            return jsonify({"error": "Erro ao processar a imagem facial"}), 400
        else:
            json_dados = cadastroPessoa(data, matrix_face)
            insercoes_db = InsercoesDb()
            resultante = insercoes_db.inserir_documento("registro_profissional", json_dados)
            if not resultante:
                return {'error': 'Erro no cadastro'}, 400
            return {'return_post': 'Cadastro realizado com sucesso!'}, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


def label_cadastro_profissional():
    try:
        filtro, projecao, opcao= {},{},[]
        buscas_db = BuscasDb(filtro, projecao, opcao)
        col_prof = list(buscas_db.retornar_dados('exibicao_cad_prof'))
        return col_prof
    except Exception as e:
        logging.error(e)
        return []


def label_consulta_turno():
    try:
        filtro, projecao, opcao = {}, {}, []
        buscas_db = BuscasDb(filtro, projecao, opcao)
        col_prof = list(buscas_db.retornar_dados('exibicao_cad_turno'))
        return col_prof
    except Exception as e:
        logging.error(e)
        return []


def label_consulta_ponto():
    try:
        filtro, projecao, opcao = {}, {}, []
        buscas_db = BuscasDb(filtro, projecao, opcao)
        col_prof = list(buscas_db.retornar_dados('exibicao_consul_ponto'))
        return col_prof
    except Exception as e:
        logging.error(e)
        return []

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
    if not ls:
        return []
    if ls:
        return ls

def carregar_registros_ponto():
    busca = BuscasDb()
    ls = list(busca.retornar_dados("registro_ponto"))
    if not ls:
        return []
    if ls:
        return ls

def carregar_perfis():
    busca = BuscasDb()
    ls = list(busca.retornar_dados("perfil"))
    if not ls:
        return []
    if ls:
        return ls


def carregar_turnos():
    busca = BuscasDb()
    ls = list(busca.retornar_dados("definicao_turno"))
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

class Turnos(Resource):
    @staticmethod
    def convert_types(document):
        """Converte campos ObjectId e datetime para tipos serializáveis."""
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, datetime.datetime):
                document[key] = value.isoformat()
            elif isinstance(value, list):
                document[key] = [
                    Turnos.convert_types(v) if isinstance(v, dict) else v
                    for v in value
                ]
            elif isinstance(value, dict):
                document[key] = Turnos.convert_types(value)
        return document

    def get(self):
        try:
            global turnos
            nr_seq_empresa_token = retornar_dados_autenticacao(request.cookies.get("auth_token"), 'nr_seq_empresa')
            turnos_ = []
            for tur in turnos:
                empresa_id = tur.get("nr_seq_empresa")
                if empresa_id and str(empresa_id) == nr_seq_empresa_token:
                    turno_convertido = Turnos.convert_types(tur.copy())
                    turnos_.append(turno_convertido)
            return turnos_, 200  # Retorne dict/list + status, não jsonify

        except Exception as e:
            return {"error": str(e)}, 500  # Mesma coisa aqui

    def post(self):
        try:
            data = request.get_json()
            nr_seq_empresa_token = retornar_dados_autenticacao(request.cookies.get("auth_token"), 'nr_seq_empresa')
            if not data:
                return {"error": "Dados não fornecidos"}, 400
            if isinstance(data, list) and len(data) >= 2:
                acao = data[1]['acao']
                if acao == 'inserir':
                    return cadastrar_turno(data[0], nr_seq_empresa_token)
                if acao == 'deletar':
                    return logging.info('metodo não implementado')
                if acao == 'atualizar':
                    return atualizar_turno(data)
                else:
                    logging.info('nada foi encontrado')
            else:
                return jsonify({"error": "Dados fornecidos não válidos"}), 400

            if isinstance(data, dict) and data.get("acao") == "inserir":
                return {"return_post": "Cadastro do turno realizado com sucesso"}, 200

            return {"error": "Formato de dados inválido ou ação desconhecida"}, 400

        except Exception as e:
            logging.error({"error a": str(e)})
            return {"error": str(e)}, 500


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
            nr_seq_empresa_token = retornar_dados_autenticacao(request.cookies.get("auth_token"), 'nr_seq_empresa')
            profs = []
            for prof in profissionais:
                if prof.get("nr_seq_empresa") and str(prof["nr_seq_empresa"]) == nr_seq_empresa_token:
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
            if isinstance(data, list) and len(data) >= 2:
                acao = data[1]['acao']
                if acao == 'inserir':
                    return cadastrar_pessoa(data[0])
                if acao == 'deletar':
                    return logging.info('metodo não implementado')
                if acao == 'atualizar':
                    return atualizar_pessoa(data)
                else:
                    logging.info('nada foi encontrado')
            else:
                return jsonify({"error": "Dados fornecidos não válidos"}), 400
        except Exception as e:
            logging.error('erro no metodo post da Classe Usuario', e)

class Exibicao(Resource):

    def post(self):
        try:
            data = request.get_json()
            tipo = data.get('tipo_exibicao')
            if tipo == "consulta_ponto":
                return [Usuario.convert_types(lab.copy()) for lab in label_ponto]
            elif tipo == "consulta_profissional":
                return [Usuario.convert_types(lab.copy()) for lab in label_prof]
            elif tipo == "consulta_turno" or tipo == "cadastro_turnos":
                return [Usuario.convert_types(lab.copy()) for lab in label_turnos]
            else:
                return []

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

    def get(self):
        try:
            global pontos
            nr_seq_empresa_token = retornar_dados_autenticacao(request.cookies.get("auth_token"), 'nr_seq_empresa')
            pontos_ = []
            for ponto in pontos:
                if ponto.get("nr_seq_empresa") and str(ponto["nr_seq_empresa"]) == nr_seq_empresa_token:
                    ponto_convertido = Usuario.convert_types(ponto.copy())
                    pontos_.append(ponto_convertido)
            return jsonify(pontos_)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


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

class Acessos(Resource):
    def get(self):
        try:
            data_acesso = datetime.datetime.fromisoformat(retornar_dados_autenticacao(request.cookies.get("auth_token"),"dt_acesso"))
            if (datetime.datetime.now() - data_acesso).seconds > 3600:
                return {"error": "Token expirado"}, 401
            response = {"dados_perfil": {"nm_perfil":retornar_dados_autenticacao(request.cookies.get("auth_token"), "nm_perfil"),
                                     "consulta_profissional": retornar_dados_autenticacao(request.cookies.get("auth_token"), 'consulta_profissional'),
                                     "consulta_ponto": retornar_dados_autenticacao(request.cookies.get("auth_token"), 'consulta_ponto'),
                                     "consulta_servicos": retornar_dados_autenticacao(request.cookies.get("auth_token"), 'consulta_servicos'),
                                     "consulta_turnos": retornar_dados_autenticacao(request.cookies.get("auth_token"),'consulta_turnos'),
                                     "cadastro_turnos": retornar_dados_autenticacao(request.cookies.get("auth_token"),'cadastro_turnos'),
                                     "cadastro_profissionais": retornar_dados_autenticacao(request.cookies.get("auth_token"),'cadastro_profissionais'),
                                     "registrar": retornar_dados_autenticacao(request.cookies.get("auth_token"),'registrar'),
                                     "configuracoes": retornar_dados_autenticacao(request.cookies.get("auth_token"),'configuracoes'),
                                     "nr_seq_empresa": retornar_dados_autenticacao(request.cookies.get("auth_token"),'nr_seq_empresa')}}, 200
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

### Busca usuários da empresa / Cadastra usuários na empresa
api.add_resource(Usuario, '/usuario')

### Busca turnos da empresa / Cadastra turnos na empresa
api.add_resource(Turnos, '/turnos')

### Busca dados para exibição no frontend / Lista acessos permitidos no frontend
api.add_resource(Exibicao, '/exibicao')
api.add_resource(Acessos, '/listar_acessos')

### Reconhece usuário para registro de ponto / Registra o ponto do usuário reconhecido
api.add_resource(Reconhecimento, '/reconhecer_credenciais')
api.add_resource(Registro, '/registro_ponto')

### Realiza autenticação
api.add_resource(Autenticacao, '/login')

# Adicionando os recursos estáticos do Front'end
api.add_resource(Home,'/')
api.add_resource(Assets,'/assets/<string:filename>')
api.add_resource(Animacoes, '/gifs/<string:filename>')

if __name__ == '__main__':
    #import dlib print(dlib.DLIB_USE_CUDA, 'Para processamento GPU')
    acessos = carregar_acesso()
    perfis = carregar_perfis()
    turnos = carregar_turnos()
    pontos = carregar_registros_ponto()
    matrix_conhecidas = carregar_matrix()
    profissionais = carregar_profissional()
    rostos_conhecidos, nomes_dos_rostos, _id = localizar_cadastros()

    label_ponto = label_consulta_ponto()
    label_turnos = label_consulta_turno()
    label_prof = label_cadastro_profissional()
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
