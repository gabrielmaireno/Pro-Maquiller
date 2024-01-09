# Pro-Maquiller

  Software de detecção de rosto com captura da cor da pele que serve para comparação com vários tipos de maquiagem, afim de conceder uma idicação que possa ajudar a encontrar a maquiagem mais natural à pele.

# Funcionamento

  A primeira etapa do projeto é a alocação e o processamento da imagem enviada pelo usuário. Ao se deparar com o programa, o usuário precisará fazer o envio da sua foto de rosto. É recomendado seguir algumas dicas para obter um resultado perfeito, sendo elas:

  - Tirar a foto com expressões naturais;

  - Conferir se o rosto todo está na foto e centralizado;

  - Tirar a foto com iluminação ambiente.

  Após receber a imagem, o algoritmo realizará uma análise facial e dividirá o rosto do usuário em um quadrante. Em seguida, esse quadrante será subdividido em três pequenos quadrados de 10x10 pixels. Um desses quadrados será posicionado na região do nariz, enquanto os outros dois serão colocados em cada uma das bochechas. Essa divisão permitirá uma análise mais detalhada das cores nessas áreas específicas do rosto.

![Exemplo](https://github.com/gabrielmaireno/Pro-Maquiller/assets/73539365/a8305071-704d-4dfe-8850-8cae0427581e)

# Video de Demonstração

https://github.com/gabrielmaireno/Pro-Maquiller/assets/73539365/39108a36-154f-45dd-b3ef-8312a3c87802

# Referências

+ Welcome to Flask. Flask, 2010. Disponível em: < https://flask.palletsprojects.com/en/2.3.x/ >
+ mediapipe. GitHub, 2023. Disponível em: < https://github.com/google/mediapipe >
+ Animate On Scroll Library. GitHub, 2018. Disponível em: < https://michalsnik.github.io/aos/ >
+ thispersondoesnotexist. thispersondoesnotexist, 2019. Disponível em: < https://thispersondoesnotexist.com >
