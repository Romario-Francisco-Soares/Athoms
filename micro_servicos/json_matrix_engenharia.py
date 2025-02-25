import face_recognition as fr
import os
import json
import numpy as np

DIRETORIO_IMAGENS_N_REGISTRADAS = '../dinamico/im_nao_registradas/'
DIRETORIO_IMAGENS_REGISTRADAS = '../dinamico/im_registradas/'

# Função para reconhecer se há rostos na foto
def reconhece_face(url_foto):
    foto = fr.load_image_file(url_foto)  # Carrega a imagem do arquivo usando o caminho correto
    rostos = fr.face_encodings(foto)  # Encontra as codificações dos rostos
    if len(rostos) > 0:  # Se houver rostos encontrados
        return True, rostos
    return False, []

# Função para mapear os arquivos no diretório de imagens
def mapear_diretorio(diretorio):
    caminhos = [os.path.join(diretorio, nome) for nome in os.listdir(diretorio)]  # Caminhos completos dos arquivos
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]  # Filtra somente arquivos
    jpgs = [arq for arq in arquivos if arq.lower().endswith(".jpg")]  # Filtra arquivos .jpg
    return jpgs

def movimentar_arquivos(de, para, nm_arquivo, extensao):
    """Movimenta arquivo DE - PARA.
       Nm_arquivo é a junção do caminho com o nome do arquivo, em seguida adicionada a extensão"""
    try:
        # Monta o caminho para o arquivo de origem e destino
        origem = os.path.join(de, f'{nm_arquivo}.{extensao}')
        destino = os.path.join(para, f'{nm_arquivo}.{extensao}')
        # Verifica se o arquivo existe
        if os.path.exists(origem):
            os.rename(origem, destino)
        else:
            raise FileNotFoundError(f"Arquivo {origem} não encontrado.")
    except Exception as erro:
        print(erro)

def get_rostos():
    rostos_conhecidos = []  # Lista para armazenar codificações de rostos conhecidos
    # Obtém os caminhos das imagens de rostos e seus nomes
    rostos_imagens = mapear_diretorio(DIRETORIO_IMAGENS_N_REGISTRADAS)
    # Para cada imagem, tenta reconhecer um rosto
    for diretorio_rosto in rostos_imagens:
        nome_arquivo = os.path.splitext(os.path.basename(diretorio_rosto))[0]
        face_reconhecida = reconhece_face(diretorio_rosto)  # Passa o caminho da imagem (diretorio_rosto)

        if face_reconhecida[0]:  # Se houver rostos reconhecidos
            valor = face_reconhecida[1][0]
            json_escrito = { "nm_arquivo":nome_arquivo,
                            "matrix":np.array(valor)}
            rostos_conhecidos.append(json_escrito)  # Adiciona o primeiro rosto encontrado (codificação)
            movimentar_arquivos(DIRETORIO_IMAGENS_N_REGISTRADAS, DIRETORIO_IMAGENS_REGISTRADAS, nome_arquivo, 'jpg')
    return rostos_conhecidos

def retornar_json_faces_integracao():
    rostos_conhecidos = get_rostos()
    for rosto in rostos_conhecidos:
        rosto['matrix'] = rosto['matrix'].tolist()
    rostos_json = json.dumps(rostos_conhecidos, indent=4)
    return rostos_json


# Exemplo de como comparar rostos conhecidos com um rosto desconhecido
#def comparar_rostos(rostos_conhecidos, rosto_desconhecido):
#    resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)  # Compara os rostos conhecidos com o rosto desconhecido
#    return resultados

# Exemplo de uso
# Aqui você deve fornecer uma codificação de um rosto desconhecido para comparar com os rostos conhecidos
# Por exemplo, vamos usar o rosto de uma nova imagem:
#rosto_desconhecido = fr.face_encodings(fr.load_image_file('./dinamico/imagens/desconhecido.png'))[0]

# Agora, vamos comparar os rostos conhecidos com o rosto desconhecido
#resultados = comparar_rostos(rostos_conhecidos, rosto_desconhecido)
  # Isso retornará uma lista de True/False, indicando se há correspondência entre os rostos
