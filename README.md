
# Detecção de Sonolência com OpenCV e MediaPipe

Este projeto utiliza **OpenCV**, **Mediapipe** e **Pygame** para detectar sinais de sonolência em motoristas através do cálculo de dois parâmetros principais:

- **EAR (Eye Aspect Ratio)**: Mede a abertura dos olhos.
- **MAR (Mouth Aspect Ratio)**: Mede a abertura da boca.

O programa também inclui um **alarme sonoro** que é acionado quando o usuário mantém os olhos fechados por um determinado tempo ou quando a boca fica aberta por muito tempo, indicando sinais de cansaço ou distração.

Este projeto foi **apresentado na 21ª Semana Nacional de Ciência, Tecnologia e Inovação**, realizada em Brasília, DF, entre os dias **05 a 10 de novembro**.

## Funcionalidades

- **Detecção de olhos e boca**: Usa landmarks faciais para calcular a razão de aspecto dos olhos e da boca.
- **Alarme sonoro**: Toca um som de alerta quando o tempo com os olhos fechados excede um limiar específico ou a boca permanece aberta por muito tempo.
- **Processamento em tempo real**: Realiza a captura de vídeo da câmera e aplica a detecção de sonolência em tempo real.

## Bibliotecas Utilizadas

- **OpenCV**: Para captura de vídeo e manipulação de imagens.
- **Mediapipe**: Para detecção de landmarks faciais.
- **NumPy**: Para cálculos matemáticos nos vetores de landmarks.
- **Pygame**: Para inicializar o áudio e tocar o alarme sonoro.

## Instalação

1. Instale as bibliotecas necessárias:

    ```bash
    pip install opencv-python mediapipe numpy pygame
    ```

2. Adicione um arquivo de áudio (por exemplo, `sonscerrado.mp3` ou `car-horn-155026.mp3`) na pasta do projeto para ser usado como som de alerta.

## Como Funciona

### Calcular EAR (Eye Aspect Ratio)

O EAR é calculado usando a distância entre pontos dos olhos detectados. Se o EAR estiver abaixo de um limiar (configurável), o sistema considera que os olhos estão fechados.

### Calcular MAR (Mouth Aspect Ratio)

O MAR é calculado usando a distância entre pontos da boca. Se o MAR estiver acima de um limiar (configurável), considera-se que a boca está aberta.

### Alarme Sonoro

Quando o EAR permanece abaixo do limiar por um certo tempo (configurável), o alarme é ativado. O alarme também é acionado se o MAR indicar que a boca está aberta.

## Código Exemplo

Aqui está um trecho de código para iniciar a detecção de sonolência:

```python
import cv2
import mediapipe as mp
import numpy as np
import time
import pygame

# Inicialização das variáveis e configurações do MediaPipe e Pygame
pygame.mixer.init()
pygame.mixer.music.load("sonscerrado.mp3")

ear_limiar = 0.27
mar_limiar = 0.1
cap = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Função para cálculo do EAR e MAR (descritas acima)
# Captura de vídeo e processamento dos frames
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()  # Processamento do frame com detecção de olhos e boca...
        # Limiar e Configurações
        # EAR: Threshold para detecção de olhos fechados. Ajustável.
        # MAR: Threshold para detecção de boca aberta. Ajustável.
        # Alarme: Configurado para tocar após 1.5 segundos com olhos fechados.
```

## Instruções de Execução

1. Conecte a câmera do dispositivo.
2. Execute o código com o comando:

    ```bash
    python nome_do_arquivo.py
    ```

3. A janela da câmera será exibida com a detecção e os alarmes ativados conforme a condição de sonolência for detectada.

## Referências

- [Documentação do OpenCV](https://docs.opencv.org/)
- [Documentação do MediaPipe](https://mediapipe.dev/)
- [Documentação do Pygame](https://www.pygame.org/docs/)



