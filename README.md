# Trekking

  

## Guia de intalação para o Linux

  

###

  

  

### Instalação do Visual Studio Code

  

1. Faça o download e instalação do [Visual Studio Code](https://code.visualstudio.com/)

  

2. Abra um terminal na pasta de downloads ou na pasta que o download foi feito e execute

``sudo apt install ./nomeDoArquivo.deb``

  

3. Recomenda-se a intalação das extensões listada abaixo. Para instalar extensões no VSCode basta ir na side bar, clicar em extensões e no menu de busca procurar pela extensão.

- Better C++ Sintax;

- C/C++;

- C/C++ Extension Pack;

- GitKraken;

- GitLens;

  

### Instalação das biblioteca


#### Dependências gerais

``sudo apt install -y ffmpeg git cmake build-essential``
``sudo apt install -y g++ cmake make git libgtk2.0-dev pkg-config``

#### OpenCV

  

1. Faça o download da ultima release do [OpenCV](https://opencv.org/releases/).

  

2. No caso o opencv não possui relese para o linux, então siga o seguinte [Guia de instalção](https://docs.opencv.org/3.4/d7/d9f/tutorial_linux_install.html).

  
3. mkdir -p build && cd build


4. cmake ../opencv


5. make -j4


6. sudo make install



### Configurando o projeto

  

1. Clone este repositório para o local desejado abrindo um terminal na pasta e rodando o comando

``git clone https://github.com/teamTroia/trekking``
  

3. Complile o programa entrando na raiz do repositorio e rodando os comandos

``cd ..``

``mkdir build && cd build``

``cmake ..``

``make``
  

4. Para rodar o projeto basta abrir o executável através do comando abaixo, rodando-o na raiz do projeto

``cd ..``

``./visaoC``
