import numpy as np
import face_recognition as fr
from colecoes.colecoes import BuscasDb

def localizar_cadastros() -> [[object], str]:
    buscas_db = BuscasDb()
    colProf = buscas_db.retornar_dados('registro_profissional')
    lista_cadastros = colProf
    matrix = []
    nomes = []
    for ls in lista_cadastros:
        print(np.__version__)
        #nomes.append(ls["nm_pessoa_fisica"])
        frame = np.array(ls["matrix_face"])
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
        localizacao_dos_rostos = fr.face_locations(rgb_frame) -- aqui tem erro
        print(localizacao_dos_rostos)
        x = fr.face_encodings(localizacao_dos_rostos)

        matrix.append(x)
    return matrix, nomes


# Aqui você pode adicionar mais operações se necessário, como manipulação de JSON, etc.
