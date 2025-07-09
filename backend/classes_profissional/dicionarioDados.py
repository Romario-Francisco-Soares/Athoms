from datetime import datetime

def _parse_date(date_str):
    """Converte string para datetime ISO 8601, retorna None se inválido."""
    try:
        return datetime.fromisoformat(date_str).isoformat() if date_str else None
    except ValueError:
        return None


def cadastroPessoa(data, matrix_face):
    json_dados = {
        "nm_pessoa_fisica": data.get('nome'),
        "data_nascimento": _parse_date(data.get('dataNascimento')),
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
        "data_cadastro_original": _parse_date(data.get('data_cadastro_original')),
        "data_contratacao": _parse_date(data.get('data_contratacao')),
        "data_ult_alteracao": _parse_date(data.get('data_ult_alteracao')),
        "nr_seq_prof_ult_alter": data.get('nr_seq_prof_ult_alter'),
        "nr_seq_prof_cadastro": data.get('nr_seq_prof_cadastro'),
        "nr_seq_prof_contratacao": data.get('nr_seq_prof_contratacao')
    }

    return json_dados