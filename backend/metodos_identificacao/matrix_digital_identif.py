import numpy as np
import face_recognition as fr
import cv2
from regras_api.json_buscar_matrix import localizar_cadastros

melhor_matrix = ''
melhor_nome = ''
melhor_id = ''

def identificador_face():
    # Carrega os rostos conhecidos
    rostos_conhecidos, nomes_dos_rostos = localizar_cadastros()
    video_capture = cv2.VideoCapture(0)
    detectado = False
    raio_x = 150  # Raio do eixo X da elipse (horizontal)
    raio_y = 200  # Raio do eixo Y da elipse (vertical, mais longo)

    while detectado == False:
        ret, frame = video_capture.read()

        # Conversão de BGR para RGB (OpenCV usa BGR por padrão)
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

        # Obtém as dimensões da imagem (altura e largura)
        h, w, _ = frame.shape
        centro_x, centro_y = w // 2, h // 2  # Calcula o centro da imagem

        # Desenha a elipse no centro da tela
        cv2.ellipse(frame, (centro_x, centro_y), (raio_x, raio_y), 0, 0, 360, (0, 255, 0), 2)

        # Detecta rostos
        localizacao_dos_rostos = fr.face_locations(rgb_frame)
        rosto_desconhecidos = fr.face_encodings(rgb_frame, localizacao_dos_rostos)

        # Lista para armazenar distâncias das faces
        distancias_faces = []

        print(rostos_conhecidos, rosto_desconhecidos)
        for (top, right, bottom, left), rosto_desconhecido in zip(localizacao_dos_rostos, rosto_desconhecidos):
            # Calcula o centro do rosto
            rosto_centro_x = (left + right) // 2
            rosto_centro_y = (top + bottom) // 2

            # Calcula a distância entre o centro do rosto e o centro da elipse
            distancia = np.sqrt((rosto_centro_x - centro_x) ** 2 + (rosto_centro_y - centro_y) ** 2)
            distancias_faces.append((distancia, (top, right, bottom, left), rosto_desconhecido))

        # Se houver rostos detectados
        if distancias_faces:
            # Ordena as faces pela distância (menor distância = mais próxima)
            distancias_faces.sort(key=lambda x: x[0])

            # A face mais próxima é a primeira
            _, (top, right, bottom, left), rosto_desconhecido = distancias_faces[0]

            # Verifica se a face está dentro da elipse (distância <= raio)
            if (abs((left + right) // 2 - centro_x) / raio_x) ** 2 + (abs((top + bottom) // 2 - centro_y) / raio_y) ** 2 <= 1:
                # Compara a face mais próxima com as conhecidas
                resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)
                face_distances = fr.face_distance(rostos_conhecidos, rosto_desconhecido)
                # Encontra o rosto mais similar
                melhor_id = np.argmin(face_distances)
                if resultados[melhor_id]:
                    melhor_matrix = rostos_conhecidos[melhor_id]
                    melhor_nome = nomes_dos_rostos[melhor_id]
                    detectado = True
                else:
                    melhor_nome = "Não detectado"

                # Desenha o retângulo ao redor da face mais próxima
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Desenha o texto com o nome
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, melhor_nome, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Exibe o quadro da webcam com a elipse
        #cv2.imshow('Webcam_facerecognition', frame)

        # Aguardar até que o usuário pressione a tecla 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return melhor_nome, melhor_id, melhor_matrix
