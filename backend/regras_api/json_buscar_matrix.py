import numpy as np
import cv2
import face_recognition as fr
from colecoes.colecoes import BuscasDb


def localizar_cadastros() -> [[object], str]:
    buscas_db = BuscasDb()
    colProf = buscas_db.retornar_dados('registro_profissional')
    lista_cadastros = colProf
    matrix = []
    nomes = []
    for ls in lista_cadastros:
        nomes.append(ls["nm_pessoa_fisica"])
        matrix.append(ls["matrix_face"])
    return matrix, nomes
