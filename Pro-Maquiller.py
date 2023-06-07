import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial import distance
from cores_referencia import cores_referencia

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

IMAGE_FILES = ["images/image.jpg"]
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5
) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)

        # Converte a imagem BGR para RGB e a processa utiliando o Mediapipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        #/////////////////////////////////////////////////////////////////////////////////////////
        if not results.detections:
            continue
        annotated_image = image.copy()
        hsv_image = cv2.cvtColor(
            image, cv2.COLOR_BGR2HSV
        )  # Converter para espaço de cores HSV
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            # Coordenadas normalizadas (entre 0 e 1) do quadrado de detecção
            xmin = int(bbox.xmin * image.shape[1])
            ymin = int(bbox.ymin * image.shape[0])
            width = int(bbox.width * image.shape[1])
            height = int(bbox.height * image.shape[0])

            # Desenhar o retângulo do quadrado de detecção
            cv2.rectangle(
                annotated_image,
                (xmin, ymin),
                (xmin + width, ymin + height),
                (0, 255, 0),
                2,
            )

            # Coordenadas de um ponto específico dentro da bbox

            # Bochecha Direita
            ponto_x1 = xmin + int(width * 0.25)

            # Nariz
            ponto_x2 = xmin + int(width * 0.5)

            # Bochecha Esquerda
            ponto_x3 = xmin + int(width * 0.75)

            # ===========================================================
            
            ponto_y = ymin + int(
                height * 0.5
            )  # Exemplo: ponto no centro vertical da bbox

            # Coletar a cor do ponto específico no espaço de cores HSV
            cor_ponto1 = image[ponto_y:ponto_y+10, ponto_x1:ponto_x1+10]

            cor_ponto2 = image[ponto_y:ponto_y+10, ponto_x2:ponto_x2+10]

            cor_ponto3 = image[ponto_y:ponto_y+10, ponto_x3:ponto_x3+10]
           

            # Desenhar um retangulo no ponto específico
            cv2.rectangle(annotated_image, (ponto_x1, ponto_y), (ponto_x1+10, ponto_y+10), (255, 0, 0), 1)
            cv2.rectangle(annotated_image, (ponto_x2, ponto_y), (ponto_x2+10, ponto_y+10), (0, 255, 0), 1)
            cv2.rectangle(annotated_image, (ponto_x3, ponto_y), (ponto_x3+10, ponto_y+10), (0, 0, 255), 1)

            # =============================================================

            #Define a média das cores dentro dos pixels

            def mediaCores(array):
                media_cores = []
                for i in range(3):
                    media = np.mean(array[:,:,i])
                    media_cores.append(media)   
                return media_cores
            
            # =============================================================

            # Valores do ponto 1
            
            cor_ponto1Total = mediaCores(cor_ponto1)
            
            # Valores do ponto 2
  
            cor_ponto2Total = mediaCores(cor_ponto2)

            # Valores do ponto 3

            cor_ponto3Total = mediaCores(cor_ponto3)

            media_rel = [(a + b + c) / 3 for a, b, c in zip(cor_ponto1Total, cor_ponto2Total, cor_ponto3Total)]
            print("media real: ",media_rel)
            
# ========================================================================================================================== 


# Define uma função para calcular a distância Euclidiana entre duas cores
def calcular_distancia(cor1, cor2):
    calculo = distance.euclidean(cor1, [cor2[0],cor2[1],cor2[2]])
    return calculo
    



# Obtém a cor atual (media_rel) que você deseja identificar
cor_atual = tuple(media_rel)

# Inicializa a menor distância como um valor alto para comparação
menor_distancia = float('inf')
cor_identificada = None

# Itera sobre as cores de referência e encontra a cor mais próxima
for cor_ref in cores_referencia:
    distancia = calcular_distancia(cor_atual, cor_ref)
    if distancia < menor_distancia:
        menor_distancia = distancia
        cor_identificada = cor_ref

# Exibe a cor identificada
print("Cor identificada:", cor_identificada[3])


# =============================================================


#Criação do quadrado com a cor da pessoa

cor = (media_rel[0], media_rel[1], media_rel[2])  # Vermelho (em BGR)

#métricas para a criação do quadrado
x_quad = image.shape[1] - 100
y_quad = 10
width_quad = 90
height_quad = 90


#criação do quadrado com cv2
cv2.rectangle(annotated_image, (x_quad, y_quad), (x_quad + width_quad, y_quad + height_quad), (cor), -1)

# =============================================================

#Criação do texto

texto = cor_identificada[3]
posicao_texto = (10, 50)  # Posição do texto na imagem
fonte = cv2.FONT_HERSHEY_SIMPLEX
escala_fonte = 1
cor_fonte = (255, 255, 255)  # Cor do texto em BGR
espessura_linha = 2
cv2.putText(annotated_image, texto, posicao_texto, fonte, escala_fonte, cor_fonte, espessura_linha)

# =============================================================

#Mostra a imagem

cv2.imshow("Tela com Cor Específica", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# =============================================================
