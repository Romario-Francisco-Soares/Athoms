import json
from typing import Optional
from datetime import date, time, datetime

class class_competencias:
    def __init__(self,
                 nr_seq_profissional: int,
                 nr_sequencia: int,
                 ds_tecnico_a: Optional[str],
                 ds_tecnico_b: Optional[str],
                 ds_tecnico_c: Optional[str],
                 ds_graduacao_a: Optional[str],
                 ds_graduacao_b: Optional[str],
                 ds_graduacao_c: Optional[str],
                 ds_espec_a: Optional[str],
                 ds_espec_b: Optional[str],
                 ds_espec_c: Optional[str],
                 ds_mba_a: Optional[str],
                 ds_mba_b: Optional[str],
                 ds_mba_c: Optional[str],
                 ds_mestrado_a: Optional[str],
                 ds_mestrado_b: Optional[str],
                 ds_mestrado_c: Optional[str],
                 ds_doutor_a: Optional[str],
                 ds_doutor_b: Optional[str],
                 ds_doutor_c: Optional[str],
                 ds_phd_a: Optional[str],
                 ds_phd_b: Optional[str],
                 ds_phd_c: Optional[str],
                 ds_curso_compl_a: Optional[str],
                 ds_curso_compl_b: Optional[str],
                 ds_curso_compl_c: Optional[str],
                 ds_curso_compl_d: Optional[str],
                 ds_curso_compl_e: Optional[str],
                 ds_curso_compl_f: Optional[str],
                 ds_curso_compl_g: Optional[str],
                 data_cadastro_original: date,
                 nr_seq_prof_cadastro: int,
                 data_ult_alteracao: Optional[date],
                 nr_seq_prof_ult_alter: Optional[int]):
        self.nr_seq_profissional = nr_seq_profissional
        self.nr_sequencia = nr_sequencia
        self.ds_tecnico_a = ds_tecnico_a
        self.ds_tecnico_b = ds_tecnico_b
        self.ds_tecnico_c = ds_tecnico_c
        self.ds_graduacao_a = ds_graduacao_a
        self.ds_graduacao_b = ds_graduacao_b
        self.ds_graduacao_c = ds_graduacao_c
        self.ds_espec_a = ds_espec_a
        self.ds_espec_b = ds_espec_b
        self.ds_espec_c = ds_espec_c
        self.ds_mba_a = ds_mba_a
        self.ds_mba_b = ds_mba_b
        self.ds_mba_c = ds_mba_c
        self.ds_mestrado_a = ds_mestrado_a
        self.ds_mestrado_b = ds_mestrado_b
        self.ds_mestrado_c = ds_mestrado_c
        self.ds_doutor_a = ds_doutor_a
        self.ds_doutor_b = ds_doutor_b
        self.ds_doutor_c = ds_doutor_c
        self.ds_phd_a = ds_phd_a
        self.ds_phd_b = ds_phd_b
        self.ds_phd_c = ds_phd_c
        self.ds_curso_compl_a = ds_curso_compl_a
        self.ds_curso_compl_b = ds_curso_compl_b
        self.ds_curso_compl_c = ds_curso_compl_c
        self.ds_curso_compl_d = ds_curso_compl_d
        self.ds_curso_compl_e = ds_curso_compl_e
        self.ds_curso_compl_f = ds_curso_compl_f
        self.ds_curso_compl_g = ds_curso_compl_g
        self.data_cadastro_original = data_cadastro_original
        self.nr_seq_prof_cadastro = nr_seq_prof_cadastro
        self.data_ult_alteracao = data_ult_alteracao
        self.nr_seq_prof_ult_alter = nr_seq_prof_ult_alter

    def criar_json(self):
        return {
            "nr_seq_profissional": self.nr_seq_profissional,
            "nr_sequencia": self.nr_sequencia,
            "ds_tecnico_a": self.ds_tecnico_a,
            "ds_tecnico_b": self.ds_tecnico_b,
            "ds_tecnico_c": self.ds_tecnico_c,
            "ds_graduacao_a": self.ds_graduacao_a,
            "ds_graduacao_b": self.ds_graduacao_b,
            "ds_graduacao_c": self.ds_graduacao_c,
            "ds_espec_a": self.ds_espec_a,
            "ds_espec_b": self.ds_espec_b,
            "ds_espec_c": self.ds_espec_c,
            "ds_mba_a": self.ds_mba_a,
            "ds_mba_b": self.ds_mba_b,
            "ds_mba_c": self.ds_mba_c,
            "ds_mestrado_a": self.ds_mestrado_a,
            "ds_mestrado_b": self.ds_mestrado_b,
            "ds_mestrado_c": self.ds_mestrado_c,
            "ds_doutor_a": self.ds_doutor_a,
            "ds_doutor_b": self.ds_doutor_b,
            "ds_doutor_c": self.ds_doutor_c,
            "ds_phd_a": self.ds_phd_a,
            "ds_phd_b": self.ds_phd_b,
            "ds_phd_c": self.ds_phd_c,
            "ds_curso_compl_a": self.ds_curso_compl_a,
            "ds_curso_compl_b": self.ds_curso_compl_b,
            "ds_curso_compl_c": self.ds_curso_compl_c,
            "ds_curso_compl_d": self.ds_curso_compl_d,
            "ds_curso_compl_e": self.ds_curso_compl_e,
            "ds_curso_compl_f": self.ds_curso_compl_f,
            "ds_curso_compl_g": self.ds_curso_compl_g,
            "data_cadastro_original": self.data_cadastro_original.isoformat(),
            "nr_seq_prof_cadastro": self.nr_seq_prof_cadastro,
            "data_ult_alteracao": self.data_ult_alteracao.isoformat() if self.data_ult_alteracao else None,
            "nr_seq_prof_ult_alter": self.nr_seq_prof_ult_alter
        }

class class_endereco:
    def __init__(self,
                 nr_cep: str,
                 tipo_logradouro: str,
                 nome_logradouro: str,
                 nr_logradouro: str,
                 complemento: Optional[str],
                 bairro: str,
                 cidade: str,
                 estado: str,
                 pais: str):
        self.nr_cep = nr_cep
        self.tipo_logradouro = tipo_logradouro
        self.nome_logradouro = nome_logradouro
        self.nr_logradouro = nr_logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais

    def criar_json(self):
        return {
            "nr_cep": self.nr_cep,
            "tipo_logradouro": self.tipo_logradouro,
            "nome_logradouro": self.nome_logradouro,
            "nr_logradouro": self.nr_logradouro,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
            "pais": self.pais
        }

class class_profissional:
    def __init__(self,
                 nr_sequencia: int,
                 nm_pessoa_fisica: str,
                 data_nascimento: date,
                 ie_sexo: str,
                 whatsapp: Optional[str],
                 email: Optional[str],
                 estado_civil: str,
                 nm_mae: str,
                 whatsapp_mae: Optional[str],
                 nm_pai: str,
                 whatsapp_pai: Optional[str],
                 cd_pis: str,
                 cd_ctps: str,
                 cd_eleitor: str,
                 cpf: str,
                 registro_geral: str,
                 ie_qualificacao: Optional[str],
                 endereco_natural: class_endereco,
                 endereco_lagradouro: class_endereco,
                 matrix_face: Optional[str],
                 matrix_digital: Optional[str],
                 matrix_retina: Optional[str],
                 data_cadastro_original: date,
                 data_contratacao: date,
                 data_ult_alteracao: Optional[date],
                 nr_seq_prof_ult_alter: Optional[int],
                 nr_seq_prof_cadastro: int,
                 nr_seq_prof_contratacao: int):
        self.nr_sequencia = nr_sequencia
        self.nm_pessoa_fisica = nm_pessoa_fisica
        self.data_nascimento = data_nascimento
        self.ie_sexo = ie_sexo
        self.whatsapp = whatsapp
        self.email = email
        self.estado_civil = estado_civil
        self.nm_mae = nm_mae
        self.whatsapp_mae = whatsapp_mae
        self.nm_pai = nm_pai
        self.whatsapp_pai = whatsapp_pai
        self.cd_pis = cd_pis
        self.cd_ctps = cd_ctps
        self.cd_eleitor = cd_eleitor
        self.cpf = cpf
        self.registro_geral = registro_geral
        self.ie_qualificacao = ie_qualificacao
        self.endereco_natural = endereco_natural
        self.endereco_lagradouro = endereco_lagradouro
        self.matrix_face = matrix_face
        self.matrix_digital = matrix_digital
        self.matrix_retina = matrix_retina
        self.data_cadastro_original = data_cadastro_original
        self.data_contratacao = data_contratacao
        self.data_ult_alteracao = data_ult_alteracao
        self.nr_seq_prof_ult_alter = nr_seq_prof_ult_alter
        self.nr_seq_prof_cadastro = nr_seq_prof_cadastro
        self.nr_seq_prof_contratacao = nr_seq_prof_contratacao

    def criar_json(self):
        return {
            "nr_sequencia": self.nr_sequencia,
            "nm_pessoa_fisica": self.nm_pessoa_fisica,
            "data_nascimento": self.data_nascimento.isoformat(),
            "ie_sexo": self.ie_sexo,
            "whatsapp": self.whatsapp,
            "email": self.email,
            "nm_mae": self.nm_mae,
            "whatsapp_mae": self.whatsapp_mae,
            "nm_pai": self.nm_pai,
            "whatsapp_pai": self.whatsapp_pai,
            "cd_pis": self.cd_pis,
            "cd_ctps": self.cd_ctps,
            "cd_eleitor": self.cd_eleitor,
            "cpf": self.cpf,
            "registro_geral": self.registro_geral,
            "ie_qualificacao": self.ie_qualificacao,
            "endereco_natural": self.endereco_natural.criar_json(),
            "endereco_lagradouro": self.endereco_lagradouro.criar_json(),
            "matrix_face": self.matrix_face,
            "matrix_digital": self.matrix_digital,
            "matrix_retina": self.matrix_retina,
            "data_cadastro_original": self.data_cadastro_original.isoformat(),
            "data_contratacao": self.data_contratacao.isoformat(),
            "data_ult_alteracao": self.data_ult_alteracao.isoformat() if self.data_ult_alteracao else None,
            "nr_seq_prof_ult_alter": self.nr_seq_prof_ult_alter,
            "nr_seq_prof_cadastro": self.nr_seq_prof_cadastro,
            "nr_seq_prof_contratacao": self.nr_seq_prof_contratacao
        }

class class_registro_ponto:
    def __init__(self,
                 nr_seq_profissional: str,
                 data_registrada: date,
                 matrix_face: Optional[str],
                 matrix_digital: Optional[str],
                 matrix_retina: Optional[str],
                 matrix_senha: Optional[str],
                 data_registrada_original: date,
                 data_ult_alteracao: date,
                 nr_seq_prof_ult_alter: str):
        self.nr_seq_profissional = nr_seq_profissional
        self.data_registrada = data_registrada
        self.matrix_face = matrix_face
        self.matrix_digital = matrix_digital
        self.matrix_retina = matrix_retina
        self.matrix_senha = matrix_senha
        self.data_registrada_original = data_registrada_original
        self.data_ult_alteracao = data_ult_alteracao
        self.nr_seq_prof_ult_alter = nr_seq_prof_ult_alter

    def criar_json(self):
        return {
            "nr_seq_profissional": self.nr_seq_profissional,
            "data_registrada": self.data_registrada.isoformat(),
            "matrix_face": self.matrix_face,
            "matrix_digital": self.matrix_digital,
            "matrix_retina": self.matrix_retina,
            "matrix_senha": self.matrix_senha,
            "data_registrada_original": self.data_registrada_original,
            "data_ult_alteracao": self.data_ult_alteracao,
            "nr_seq_prof_ult_alter": self.nr_seq_prof_ult_alter
        }

class class_turno:
    def __init__(self,
                 desc: str,
                 ano: int,
                 mes: int,
                 semana: int,
                 dia_semana: int,
                 prev_hr_chegada: date,
                 prev_hr_saida_alm: date,
                 prev_hr_ret_alm: date,
                 prev_hr_saida: date,
                 min_intervalo: Optional[int],
                 min_tolerancia_anteced: Optional[int],
                 min_tolerancia_atraso: Optional[int]
                 ):
        self.desc = desc
        self.ano = ano
        self.mes = mes
        self.semana = semana
        self.dia_semana = dia_semana
        self.prev_hr_chegada = prev_hr_chegada
        self.prev_hr_saida_alm = prev_hr_saida_alm
        self.prev_hr_ret_alm = prev_hr_ret_alm
        self.prev_hr_saida = prev_hr_saida
        self.min_intervalo = min_intervalo
        self.min_tolerancia_anteced = min_tolerancia_anteced
        self.min_tolerancia_atraso = min_tolerancia_atraso

    def criar_json_dia(self):
        return {
            "dia_semana": self.dia_semana,
            "prev_hr_chegada": self.prev_hr_chegada,
            "prev_hr_saida_alm":  self.prev_hr_saida_alm,
            "prev_hr_ret_alm":  self.prev_hr_ret_alm,
            "prev_hr_saida":  self.prev_hr_saida,
            "min_intervalo": self.min_intervalo,
            "min_tolerancia_anteced": self.min_tolerancia_anteced,
            "min_tolerancia_atraso": self.min_tolerancia_atraso
        }

    def criar_json_semana(self):
        if self.dia_semana == 0:
            return {"segunda-feira": self.criar_json_dia()}
        if self.dia_semana == 1:
            return {"terça-feira": self.criar_json_dia()}
        if self.dia_semana == 2:
            return {"quarta-feira": self.criar_json_dia()}
        if self.dia_semana == 3:
            return {"quinta-feira": self.criar_json_dia()}
        if self.dia_semana == 4:
            return {"sexta-feira": self.criar_json_dia()}
        if self.dia_semana == 5:
            return {"sábado": self.criar_json_dia()}
        if self.dia_semana == 6:
            return {"domingo": self.criar_json_dia()}
        if self.dia_semana == 8:
            todos_dias = list()
            dias_string = ["segunda-feira", "terca-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
            for dia in range(7):
                self.dia_semana = dia
                todos_dias.append({dias_string[dia]: self.criar_json_dia()})
            self.dia_semana = 8
            return todos_dias

    def criar_json_escala(self):
        if self.semana == 1:
            return {"semana_1": self.criar_json_semana()}
        if self.semana == 2:
            return {"semana_2": self.criar_json_semana()}
        if self.semana == 3:
            return {"semana_3": self.criar_json_semana()}
        if self.semana == 4:
            return {"semana_4": self.criar_json_semana()}
        if self.semana == 5:
            return {"semana_5": self.criar_json_semana()}
        if self.semana == 6:
            return{
                "desc": self.desc,
                "ano": self.ano,
                "mes": self.mes,
                "semana_1": self.criar_json_semana(),
                "semana_2": self.criar_json_semana(),
                "semana_3": self.criar_json_semana(),
                "semana_4": self.criar_json_semana(),
                "semana_5": self.criar_json_semana()
            }
