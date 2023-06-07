import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial import distance
from flask import Flask, render_template, request, send_file
from cores_referencia import cores_referencia

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imagem_processada/<path:filename>')
def imagem_processada(filename):
    return send_file(filename, mimetype='image/jpeg')

@app.route('/upload', methods=['POST'])
def upload():
    # Obtém o arquivo enviado pelo usuário
    imagem = request.files['imagem']

    # Salva o arquivo em um diretório temporário
    imagem_temporaria = 'temp/temp.jpg'
    imagem.save(imagem_temporaria)

    # Processa a imagem e realiza o reconhecimento de cor
    cor_identificada, imagem_processada = processar_imagem(imagem_temporaria)

    # Salva a imagem processada
    imagem_processada_path = 'temp/imagem_processada.jpg'
    cv2.imwrite(imagem_processada_path, imagem_processada)

    # Retorna a cor identificada e o caminho da imagem processada para o front-end
    return render_template('index.html', cor_identificada=cor_identificada, imagem_path=imagem_processada_path)

def processar_imagem(imagem_path):
    # Código de processamento da imagem (mesmo código que você compartilhou)

    IMAGE_FILES = [imagem_path]
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5
    ) as face_detection:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)

            # Converte a imagem BGR para RGB e a processa utilizando o Mediapipe Face Detection.
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Restante do código de processamento da imagem (desenho de retângulos, identificação de cor, etc.)
            
            if not results.detections:
                continue
            annotated_image = image.copy()
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                xmin = int(bbox.xmin * image.shape[1])
                ymin = int(bbox.ymin * image.shape[0])
                width = int(bbox.width * image.shape[1])
                height = int(bbox.height * image.shape[0])
                cv2.rectangle(
                    annotated_image,
                    (xmin, ymin),
                    (xmin + width, ymin + height),
                    (0, 255, 0),
                    2,
                )
                ponto_x1 = xmin + int(width * 0.25)
                ponto_x2 = xmin + int(width * 0.5)
                ponto_x3 = xmin + int(width * 0.75)
                ponto_y = ymin + int(height * 0.5)
                cor_ponto1 = image[ponto_y : ponto_y + 10, ponto_x1 : ponto_x1 + 10]
                cor_ponto2 = image[ponto_y : ponto_y + 10, ponto_x2 : ponto_x2 + 10]
                cor_ponto3 = image[ponto_y : ponto_y + 10, ponto_x3 : ponto_x3 + 10]
                cv2.rectangle(
                    annotated_image, (ponto_x1, ponto_y), (ponto_x1 + 10, ponto_y + 10), (255, 0, 0), 1
                )
                cv2.rectangle(
                    annotated_image, (ponto_x2, ponto_y), (ponto_x2 + 10, ponto_y + 10), (0, 255, 0), 1
                )
                cv2.rectangle(
                    annotated_image, (ponto_x3, ponto_y), (ponto_x3 + 10, ponto_y + 10), (0, 0, 255), 1
                )

                def mediaCores(array):
                    media_cores = []
                    for i in range(3):
                        media = np.mean(array[:, :, i])
                        media_cores.append(media)
                    return media_cores

                cor_ponto1Total = mediaCores(cor_ponto1)
                cor_ponto2Total = mediaCores(cor_ponto2)
                cor_ponto3Total = mediaCores(cor_ponto3)

                media_rel = [(a + b + c) / 3 for a, b, c in zip(cor_ponto1Total, cor_ponto2Total, cor_ponto3Total)]
                print("media real: ", media_rel)

            def calcular_distancia(cor1, cor2):
                calculo = distance.euclidean(cor1, [cor2[0], cor2[1], cor2[2]])
                return calculo

            cor_atual = tuple(media_rel)
            menor_distancia = float('inf')
            cor_identificada = None

            for cor_ref in cores_referencia:
                distancia = calcular_distancia(cor_atual, cor_ref)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    cor_identificada = cor_ref

            print("Cor identificada:", cor_identificada[3])

            cor = (media_rel[0], media_rel[1], media_rel[2])
            x_quad = image.shape[1] - 100
            y_quad = 10
            width_quad = 90
            height_quad = 90

            cv2.rectangle(annotated_image, (x_quad, y_quad), (x_quad + width_quad, y_quad + height_quad), cor, -1)

            texto = cor_identificada[3]
            posicao_texto = (10, 50)
            fonte = cv2.FONT_HERSHEY_SIMPLEX
            escala_fonte = 1
            cor_fonte = (255, 255, 255)
            espessura_linha = 2
            cv2.putText(annotated_image, texto, posicao_texto, fonte, escala_fonte, cor_fonte, espessura_linha)

            return cor_identificada, annotated_image

if __name__ == '__main__':
    app.run(debug=True)
