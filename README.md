# Reconhecimento Facial com OpenCV e MySQL

## Descrição
Este projeto implementa um sistema de reconhecimento facial utilizando OpenCV e MySQL. O sistema permite cadastrar novos usuários com nome e CPF, capturar imagens para treinamento do modelo e realizar o reconhecimento facial com base nos dados cadastrados.

## Funcionalidades
- Cadastro de usuários (Nome e CPF) com armazenamento no banco de dados MySQL.
- Captura de imagens do rosto e armazenamento local.
- Treinamento de modelo usando o algoritmo LBPH (Local Binary Pattern Histogram).
- Reconhecimento facial em tempo real.
- Interface baseada em OpenCV para exibição dos resultados.

## Tecnologias Utilizadas
- Python
- OpenCV
- MySQL
- NumPy

## Requisitos
Para executar este projeto, você precisará dos seguintes itens:
- Python 3.7+
- MySQL Server instalado e rodando
- Bibliotecas Python:
  ```sh
  pip install opencv-contrib-python numpy mysql-connector-python
  ```

## Instalação e Configuração
1. Clone este repositório:
   ```sh
   git clone https://github.com/seuusuario/ReconhecimentoPy.git
   ```
2. Configure o banco de dados MySQL:
   - Crie um banco de dados chamado `reconhecimento`
   - O sistema criará automaticamente a tabela `usuarios`.

3. Execute o script:
   ```sh
   python reconhecimento_facial.py
   ```

## Como Usar
1. **Cadastrar um novo usuário:**
   - Execute o programa e selecione a opção `1`.
   - Insira o nome e o CPF do usuário.
   - O sistema criará um diretório para armazenar as imagens do rosto.

2. **Treinar o modelo:**
   - Durante a execução, pressione a tecla `t` para treinar o modelo com as imagens capturadas.

3. **Reconhecer rostos:**
   - Durante a execução, pressione a tecla `space` para capturar imagens e cadastrar um novo rosto.
   - O sistema irá detectar e identificar o rosto de usuários já treinados.

4. **Fechar o programa:**
   - Pressione a tecla `q` para sair.

## Estrutura do Projeto
```
ReconhecimentoPy/
│── USUARIO/               # Diretório contendo as imagens de treinamento
│── reconhecimento_facial.py  # Código principal do sistema
│── haarcascade_frontalface_default.xml  # Classificador Haar para detecção facial
│── .gitignore             # Arquivos a serem ignorados pelo Git
│── README.md              # Documentação do projeto
```

## Possíveis Erros e Soluções
- **Erro ao abrir a câmera:** Certifique-se de que a webcam está conectada e funcionando.
- **Arquivo `haarcascade_frontalface_default.xml` não encontrado:** Verifique se o caminho para o arquivo está correto.
- **Erro de conexão com MySQL:** Confirme que o servidor MySQL está rodando e que as credenciais de acesso estão corretas.

## Autor
- **Pablo Moisés** - [GitHub](https://github.com/pablinrlq)


