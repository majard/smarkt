Caso não tenha a ferramenta pip, digite o seguinte comando no terminal:
$ sudo easy_install pip

Para instalar todas as dependências de forma expressa, foi utilizada a ferramenta pipenv:

$ pip install pipenv

Após instalar, apenas clone o repositório e digite no diretório com o arquivo Pipfile:

pipenv install

Isso criará um ambiente virtual isolado e instalará os pacotes necessários.

Agora temos que aplicar as migrações do Django OAuth Toolkit e criar um superusuário para ter acesso a interface que o pacote disponibiliza, vamos fazer isso com os seguintes comandos

$ python manage.py migrate

$ python manage.py createsuperuser

$ python manage.py runserver

Acessamos http://localhost:8000/admin e nos autenticamos no admin do django, agora estamos prontos para registrar nossa API de autenticação.
Registrando Aplicação de Autenticação

Agora vamos acessar http://127.0.0.1:8000/o/applications/ e vamos registrar nossa API de autenticação utilizando qualquer nome.

Client type: Confidential. Authorization grant type: resource owner password-based.

Para poder acessar os endpoints é necessário incluir o token de acesso na requisição. Para conseguir um token de acesso, podemos usar o seguinte comando:

& curl -X POST http://localhost:8000/o/token/ -H "content-type: application/x-www-form-urlencoded" -d "grant_type=password&client_id=<your client id>&client_secret=<your client secret>&username=<your username>&password=<your password>"

A resposta deve ser a seguinte

$ {"expires_in": 36000, "refresh_token": <your refresh token>, "access_token": <your access token>, "token_type": "Bearer", "scope": "read write groups"}


# **Desafio Backend:** #

O conceito desse desafio é nos ajudar a avaliar as habilidades dos candidatos às vagas de backend.

Você tem que desenvolver um sistema de estoque para um supermercado.

Esse supermercado assume que sempre que ele compra uma nova leva de produtos, ele tem que calcular o preço médio de compra de cada produto para estipular um preço de venda.
Para fins de simplificação assuma que produtos que tenham nomes iguais, são o mesmo produto e que não existe nem retirada e nem venda de produtos no sistema.

O valor calculado de preço médio deve ser armazenado.

Seu sistema deve:

1. Cadastro de produtos (Nome)
2. Compra de produtos (Produto, quantidade e preço de compra)
3. Listagem dos produtos comprados separados por compra (Nome, quantidade, preço de compra, preço médio)
4. Ser fácil de configurar e rodar em ambiente Unix (Linux ou Mac OS X)
5. Ser WEB
6. Ser escrita em Python 3.4+
7. Só deve utilizar biliotecas livres e gratuitas

Esse sistema não precisa ter, mas será um plus:

1. Autenticação e autorização (se for com OAuth, melhor ainda)
2. Ter um design bonito
3. Testes automatizados


# **Desafio Frontend:** #

O conceito desse desafio é nos ajudar a avaliar as habilidades dos candidatos às vagas de frontend.

Você tem que desenvolver um sistema de estoque para um supermercado.

A api mockada a ser utilizada fica em http://docs.querotrabalharnawpensar.apiary.io

Seu sistema deve:

1. Cadastro de produtos (Nome)
2. Compra de produtos (Produto, quantidade e preço)
3. Listagem dos produtos comprados separados por compra (Nome, quantidade, preço de compra)
4. Ser fácil de configurar e rodar em ambiente Unix (Linux ou Mac OS X)
5. Só deve utilizar biliotecas livres e gratuitas

Esse sistema não precisa ter, mas será um plus:

1. Autenticação e autorização (Facebook, Google, Twitter)
2. Ter um design bonito e responsivo
3. Testes automatizados
4. Angular / Ionic / React / ReactNative


# **Avaliação:** #

Vamos avaliar seguindo os seguintes critérios:

1. Você conseguiu concluir os requisitos?
2. Você documentou a maneira de configurar o ambiente e rodar sua aplicação?
