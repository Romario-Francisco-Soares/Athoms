from datetime import datetime
from pytz import timezone, utc
from colecoes.colecoes import registro_profissionais

def cadastrar_profissional(nome):
    colCadProf = registro_profissionais()
    local_datetime = datetime.now()
    pacific = timezone('America/Sao_Paulo')
    local_datetime = pacific.localize(local_datetime)
    utc_datetime = local_datetime.astimezone(utc)
    documento = {
        "nr_seq_profissional": f"{nome}",
        "data": utc_datetime
    }
    colCadProf.insert_one(documento)
    return True