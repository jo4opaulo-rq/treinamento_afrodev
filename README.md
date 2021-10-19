# treinamento_afrodev
3ª edição do programa afrodev, as trilhas serão patrocinadas pela Suzano S.A e pela Alelo.  Formações na linguagem Python.

# Repositório utilizado no Treinamento Avançado de Ciência de Dados:

Aqui vamos armazenar todos os recursos necessários para acompanhar o treinamento avançado de Ciência de Dados

Lembrem-se de clonar e configurar seu ambiente com antecedência para melhor aproveitar as sessões ao vivo:

## Como utilizar:

1. Instale o Git: baixe o arquivo em: https://git-scm.com/download/win e instale (não é necessário ser administrador do sistema)

2. Na barra iniciar, digite "prompt" ou "terminal", ira aparecer a opção: Prompt de Comando. Clique nela, abrindo um terminal:

3. Navegue até a pasta utilizando o comando cd <pasta> que você deseja salvar seu repositorio, exemplo: cd OneDrive

4. Clique no botão "Clone" desse respositório e copie o Link

5. No terminal, digite git clone <link>. Exemplo: git clone https://suzano@dev.azure.com/suzano/Academia_Digital/_git/Treinamento

6. Será criada automaticamente uma pasta chamada Treinamento, navegue até ela com o comando cd Treinamento

7. Certifique-se que você ja instalou o Python. Você pode fazer isso digitando no terminal: Python --version. Se não apareceu nada, você pode instalar abrindo a Central de Software na barra de inicialização, digitando python e instalar.

8. Com o Python instalado, crie um ambiente virtual. Digite no terminal o comando python -m venv my-env. Isso é feito SOMENTE NA PRIMEIRA VEZ que o projeto for executado

9. Execute os 3 comandos em sequência: cd my-venv, cd Scripts, actitvate.bat

10. Navegue de volta para a raiz do repositório: cd.., cd..

11. Instale os requirements: na pasta raiz digite pip install -r requirements.txt

12. Caso haja algum problema relacionado a SSL Error, digite: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

13. Pronto! Se deu tudo certo, agora você pode executar o jupyter notebook: digite no terminal "jupyter notebook"

14. Quando for executar novamente seu notebook: execute somente os passos 9, 10 e 13
