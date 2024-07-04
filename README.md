# Face Stalker fadiga

![Face Stalker Fadiga](https://github.com/zw0s/Face-Stalker-fadiga/blob/main/Screenshot_19.png)

O Face Stalker fadiga foi um projeto desenvolvido para a disciplina Engenharia Unificada em colaboração do [Foguete](https://github.com/FOGUETE-1995) a fim de prevenir acidentes adivindo do cansaço, o projeto consiste em um dispositivo que localiza o rosto atráves de um modelo já treinado e utiliza um ponto central (utilizamos o nariz) para se basear e seguir o rosto, assim que ele encontra um rosto ele identifica 68 pontos faciais e começa a monitorar a distância entre as pálpebras, se a distância entre os pontos superiores e inferiores das pálpebras for menor que a constante que definimos por um certo tempo ela emite um alerta na tela e um sinal sonoro.

## Funcionalidades:

- Localização de rosto utilizando modelo de aprendizado de máquina.
- Monitoramento contínuo da distância entre pálpebras.
- Alerta visual e sonoro em caso de cansaço detectado.

## Como Utilizar:

- O código python vai na raspberry pi, é ela que roda o script e controla a câmera.
- O código em c++ é utilizado na ESP32, é ela que controla os servomotores que controlam a câmera e manda as coordenadas para a raspberry pi.
- SSH é o melhor método para comtrolar a raspberry remotamente.
- A câmera segue por incremento, um controle com PID é muito mais preciso e fluído.

## Links externos:

https://pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
