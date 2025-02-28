import sys
import os
import cv2
import numpy as np
import mysql.connector

# Função para conectar ao MySQL
def mysql_get_mydb():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="reconhecimento"
    )

# Função para criar a tabela no MySQL
def create_table(cnx):
    cursor = cnx.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            cpf VARCHAR(255)
        )
    """)
    cnx.commit()

# Função para cadastrar um novo usuário
def cadastro(option):
    if option == '1':
        nome = input("Digite o nome: ")
        cpf = input("Digite o CPF: ")
        return nome, cpf
    return None, None

# Função para escolher uma opção
def choose():
    print("------------------------------------")
    print("        RECONHECIMENTO FACIAL       ")
    print("------------------------------------")
    print("1. Cadastrar novo usuário")
    print("2. Iniciar reconhecimento facial")
    return input("Opção: ")

# Conectando com o MySQL e criando a tabela
cnx = mysql_get_mydb()
create_table(cnx)

#################################################################
# Inicializando o reconhecimento facial
def creatDir(name, path=''):
    # Verifica se o diretório existe; caso contrário, cria-o
    if not os.path.exists(f'{path}/{name}'):
        os.makedirs(f'{path}/{name}')

def saveFace():
    # Cria a pasta de treino e a pasta do usuário
    global saveface
    global lastName
    saveface = True
    creatDir('USUARIO')
    print("CADASTRANDO..")
    # A variável Nome deve ter sido definida no cadastro
    name = Nome
    lastName = name
    creatDir(name, 'USUARIO')

def saveImg(img):
    # Salva as fotos na pasta do usuário, nomeando-as
    global lastName
    qtd = os.listdir(f'USUARIO/{lastName}')
    cv2.imwrite(f'USUARIO/{lastName}/{str(len(qtd))}.jpg', img)

def trainData():
    # Realiza o treinamento das fotos
    global recognizer
    global trained
    global persons
    trained = True
    persons = os.listdir('USUARIO')
    ids = []
    faces = []
    for i, p in enumerate(persons):
        # Incrementa o índice para usar como ID
        i += 1
        for f in os.listdir(f'USUARIO/{p}'):
            img = cv2.imread(f'USUARIO/{p}/{f}', 0)
            faces.append(img)
            ids.append(i)
    recognizer.train(faces, np.array(ids))
#################################################################

# Selecionador de opções
choose_option = choose()
response = cadastro(choose_option)
if choose_option == '1':
    Nome = response[0]
    cpf = response[1]
elif choose_option == '2':
    print("Vamos iniciar o reconhecimento facial")

# Variáveis globais
lastName = ''
saveface = False
savefaceC = 0
trained = False
persons = []

# Inicia a captura de vídeo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a câmera")
    sys.exit()

# Carrega o classificador Haar Cascade (altere o caminho se necessário)
face_cascade_path = 'C:\\Users\\Pablin\\Desktop\\Pablo Projetos\\Reconhecimento\\haarcascade_frontalface_default.xml'
if not os.path.exists(face_cascade_path):
    print(f"Arquivo Haar Cascade não encontrado: {face_cascade_path}")
    sys.exit()

face_cascade = cv2.CascadeClassifier(face_cascade_path)
# Carrega o recognizer (certifique-se de ter instalado opencv-contrib-python)
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Loop principal
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o frame")
        break
    # Converte o frame para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detecta os rostos no frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 6)
    
    for i, (x, y, w, h) in enumerate(faces):
        # Desenha um retângulo ao redor do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Recorta o rosto e redimensiona para 400x400
        roi_gray = gray[y:y+h, x:x+w]
        resize = cv2.resize(roi_gray, (400, 400))
        
        if trained:
            # Prediz o rosto e obtém a confiança
            idf, conf = recognizer.predict(resize)
            # Obtém o nome da pessoa com base no índice
            nameP = persons[idf-1]
            if conf < 40:
                cv2.putText(frame, nameP, (x+5, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, nameP, (x+5, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'TREINADO', (10,65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'NAO TREINADA', (10,65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
        
        if saveface:
            cv2.putText(frame, str(savefaceC), (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1, cv2.LINE_AA)
            savefaceC += 1
            saveImg(resize)
        if savefaceC > 100:
            savefaceC = 0
            saveface = False

    # Instruções na tela
    cv2.putText(frame, "Pressione a tecla 'space' para cadastrar um novo perfil.", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "Pressione a tecla 't' para realizar o reconhecimento facial.", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "Pressione a tecla 'q' para fechar.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    
    cv2.imshow('frame', frame)
    key = cv2.waitKey(10)
    
    # Treina o recognizer ao pressionar 't'
    if key == ord('t'):
        trainData()
    # Inicia o cadastro ao pressionar 'space'
    if key == ord(' '):
        saveFace()
    # Encerra o loop ao pressionar 'q'
    if key & 0xFF == ord('q'):
        break
      
cap.release()
cv2.destroyAllWindows()
