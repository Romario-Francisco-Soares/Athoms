import json
from bson import ObjectId
from datetime import datetime, timedelta, timezone
import locale

from colecoes.colecoes import InsercoesDb, BuscasDb
from classes_profissional.classesDados import class_registro_ponto, class_turno


def semana_do_mes(data: datetime) -> int:
    return ((data.day - 1) // 7) + 1


def inserir_turno(data_atual):
    turno = class_turno(
        'Turno para operadores de caixa', 2025, 7, 6, 8,
        data_atual, data_atual, data_atual, data_atual,
        15, 5, 5
    ).criar_json_escala()

    InsercoesDb().inserir_documento('definicao_turno', turno)


def pegar_hora(dt, data_base):
    return dt.replace(
        year=data_base.year,
        month=data_base.month,
        day=data_base.day,
        tzinfo=timezone.utc,
        second=0,
        microsecond=0
    )


def validar_regra_registro_ponto(id_usuario, data_atual):
    def buscar_ultimo_ponto():
        inicio = datetime(data_atual.year, data_atual.month, data_atual.day, 0, 0, 0, tzinfo=timezone.utc)
        fim = datetime(data_atual.year, data_atual.month, data_atual.day, 23, 59, 59, tzinfo=timezone.utc)
        filtro = {
            "nr_seq_profissional": id_usuario,
            "data_registrada_original": {"$gte": inicio, "$lte": fim}
        }
        projecao = {"data_registrada_original": 1, "_id": 0}

        registros = BuscasDb(filtro, projecao).retornar_dados('registro_ponto')
        return len(list(registros))

    def obter_turno_profissional():
        try:
            filtro = {"nr_sequencia_profissional": ObjectId(id_usuario)}
            projecao = {"nr_sequencia_turno": 1, '_id': 0}
            turno = list(BuscasDb(filtro, projecao).retornar_dados('definicao_profissional_turno'))
            return turno[0]["nr_sequencia_turno"] if turno else None
        except Exception as e:
            print(f"Erro ao buscar turno do profissional: {e}")
            return None

    def obter_turno(nr_seq_turno):
        try:
            filtro = {"_id": nr_seq_turno, "ano": data_atual.year, "mes": data_atual.month}
            return list(BuscasDb(filtro).retornar_dados('definicao_turno'))
        except Exception as e:
            print(f"Erro ao buscar informações do turno: {e}")
            return []

    def obter_horarios_turno(turno):
        try:
            semana = semana_do_mes(data_atual)
            nome_dia = data_atual.strftime("%A")
            chave_semana = f"semana_{semana}"
            return turno[0][chave_semana][data_atual.weekday()][nome_dia]
        except Exception as e:
            print(f"Erro ao identificar horários do turno: {e}")
            return {}

    def dentro_da_tolerancia(hora_atual, hora_prevista, antecipada, atrasada):
        if hora_atual < hora_prevista - timedelta(minutes=antecipada):
            return False, "Muito cedo"
        if hora_atual > hora_prevista + timedelta(minutes=atrasada):
            return False, "Muito tarde"
        return True, "Dentro do intervalo"

    tipo_registro = buscar_ultimo_ponto()

    turno_id = obter_turno_profissional()
    if not turno_id:
        print("Turno do profissional não encontrado.")
        return False

    turno_info = obter_turno(turno_id)
    if not turno_info:
        print("Informações do turno não encontradas.")
        return False

    locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
    horarios_turno = obter_horarios_turno(turno_info)
    if not horarios_turno:
        print("Horários do turno não disponíveis.")
        return False

    try:
        entrada = pegar_hora(horarios_turno["prev_hr_chegada"], data_atual)
        saida_alm = pegar_hora(horarios_turno["prev_hr_saida_alm"], data_atual)
        retorno_alm = pegar_hora(horarios_turno["prev_hr_ret_alm"], data_atual)
        saida = pegar_hora(horarios_turno["prev_hr_saida"], data_atual)

        antecip = horarios_turno["min_tolerancia_anteced"]
        atras = horarios_turno["min_tolerancia_atraso"]

        horario_atual = pegar_hora(data_atual, data_atual)
        ok, msg = '', ''
        if tipo_registro == 0:
            ok, msg = dentro_da_tolerancia(horario_atual, entrada, antecip, atras)
        if tipo_registro == 1:
            ok, msg = dentro_da_tolerancia(horario_atual, saida_alm, antecip, atras)
        if tipo_registro == 2:
            ok, msg = dentro_da_tolerancia(horario_atual, retorno_alm, antecip, atras)
        if tipo_registro == 3:
            ok, msg = dentro_da_tolerancia(horario_atual, saida, antecip, atras)
        if tipo_registro > 3:
            print("Registro extra-turno.")
            return True
        print(msg)
        return ok

    except Exception as e:
        print(f"Erro ao testar horários: {e}")
        return False


def registrar_ponto(nr_seq_profissional: str,
                    matrix_face: str,
                    matrix_digital: str,
                    matrix_retina: str,
                    matrix_senha: str,
                    nr_seq_prof_ult_alter: str):

    utc_now = datetime.now(tz=timezone.utc)

    if validar_regra_registro_ponto(nr_seq_profissional, utc_now):
        registro = class_registro_ponto(
            nr_seq_profissional,
            utc_now,
            matrix_face,
            matrix_digital,
            matrix_retina,
            matrix_senha,
            utc_now,
            utc_now,
            nr_seq_prof_ult_alter
        )

        resultado = InsercoesDb().inserir_documento('registro_ponto', vars(registro))
        return resultado

    return False
