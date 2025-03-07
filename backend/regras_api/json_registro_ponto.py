from datetime import datetime
from pytz import timezone, utc
from colecoes.colecoes import registro_ponto
from classes_profissional.classesDados import class_registro_ponto

def registrar_ponto(nr_seq_profissional,
                    data_registrada,
                    matrix_face,
                    matrix_digital,
                    matrix_retina,
                    matrix_senha,
                    data_registrada_original,
                    data_ult_alteracao,
                    nr_seq_prof_ult_alter):

    classe_registro = class_registro_ponto(
                        nr_seq_profissional,
                        data_registrada,
                        matrix_face,
                        matrix_digital,
                        matrix_retina,
                        matrix_senha,
                        data_registrada_original,
                        data_ult_alteracao,
                        nr_seq_prof_ult_alter)

    colRegistroPonto = registro_ponto()

    local_datetime = datetime.now()
    pacific = timezone('America/Sao_Paulo')
    local_datetime = pacific.localize(local_datetime)
    utc_datetime = local_datetime.astimezone(utc)
    documento = {
        "nr_seq_profissional": f"{classe_registro.nr_seq_profissional}",
        "data_registrada": f"{utc_datetime}",
        "matrix_face": f"{classe_registro.matrix_face}",
        "matrix_digital": f"{classe_registro.matrix_digital}",
        "matrix_retina": f"{classe_registro.matrix_retina}",
        "matrix_senha": f"{classe_registro.matrix_senha}",
        "data_registrada_original": f"{utc_datetime}",
        "data_ult_alteracao": f"{utc_datetime}",
        "nr_seq_prof_ult_alter": f"{classe_registro.nr_seq_prof_ult_alter}",
    }
    #colRegistroPonto.insert_one(documento)
    print(documento)
    return True