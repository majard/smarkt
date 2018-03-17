Caso não tenha a ferramenta pip, digite o seguinte comando no terminal:
$ sudo easy_install pip

Para instalar todas as dependências de forma expressa, foi utilizada a ferramenta pipenv:

$ pip install pipenv

No mac o equivalente é

$ brew install pipenv

Após instalar, apenas clone o repositório e digite no diretório com o arquivo Pipfile:

pipenv install

Isso criará um ambiente virtual isolado e instalará os pacotes necessários.

Se o pipenv não estiver disponível no seu shell após a instalação, você precisará adicionar o diretório binário da base de usuários ao seu PATH.

No Linux e no MacOS, você pode encontrar o diretório binário da base de usuários executando  

python -m site --user-base 

e adicionando bin ao final. Por exemplo, isso normalmente imprimirá ~ / .local (com ~ expandido para o caminho absoluto para seu diretório inicial), então você precisará adicionar ~ / .local / bin para o seu PATH. Você pode configurar seu PATH permanentemente modificando ~ / .profile.

No Windows, você pode encontrar o diretório binário da base de usuários executando 

py -m site --user-site 

e substituindo pacotes de sites com Scripts. Por exemplo, isso pode retornar os pacotes C: \ Users \ Username \ AppData \ Roaming \ Python36 \ site-packages para que você precise configurar seu PATH para incluir C: \ Users \ Nome do Usuário \ AppData \ Roaming \ Python36 \ Scripts. Você pode configurar seu PATH de usuário permanentemente no Painel de controle. Talvez seja necessário fazer o desconto para que as alterações PATH tenham efeito.

Agora temos que aplicar as migrações do Django OAuth Toolkit e criar um usuário para ter acesso a interface que o pacote disponibiliza, vamos fazer isso com os seguintes comandos

$ python manage.py migrate # para migrar a database

# opcional: cria um superusuário 
$ python manage.py createsuperuser 

Alternativamente, crie um usuário comum visitando a página principal (http://localhost:8000/) e cadastre um usuário utilizando a interface web.

$ python manage.py runserver

Acessamos http://localhost:8000/admin e nos autenticamos no admin do django, agora estamos prontos para registrar nossa API de autenticação.
Registrando Aplicação de Autenticação

Agora vamos acessar http://localhost/o/applications/ e vamos registrar nossa API de autenticação utilizando qualquer nome.

Client type: Confidential. Authorization grant type: resource owner password-based.

Para poder acessar os endpoints é necessário incluir o token de acesso na requisição. Para conseguir um token de acesso, podemos usar o seguinte comando:

& curl -X POST http://localhost:8000/o/token/ -H "content-type: application/x-www-form-urlencoded" -d "grant_type=password&client_id=<your client id>&client_secret=<your client secret>&username=<your username>&password=<your password>"

Ou fazer uma requisição POST com conteúdo equivalente utilizando outra ferramenta.

A resposta deve ser a seguinte:

$ {"expires_in": 36000, "refresh_token": <your refresh token>, "access_token": <your access token>, "token_type": "Bearer", "scope": "read write groups"}

A partir de então use o access_token no header das suas requisições http
em "Authorization" com o valor "Bearer " + access_token

Acesse a api rest nos seguintes endpoints

POST http://localhost:8000/api/products/ 
-> cria um novo produto associado ao usuário atualmente autenticado
-> Espera um chave "name" no corpo da requisição.

GET http://localhost:8000/api/products/ 
-> retorna todos os produtos do usuário atualmente autenticado

GET http://localhost:8000/api/products/<product_id>
-> retorna o produto associado a product_id

PUT http://localhost:8000/api/products/<product_id>
-> edita o nome do produto associado a product_id 

DELETE http://localhost:8000/api/products/<product_id>
-> deleta o produto associado a product_id

POST http://localhost:8000/api/products/ 
-> cria uma nova associado ao usuário atualmente autenticado
-> Espera as chaves "name", "quantity" e "price" no corpo da requisição.

GET http://localhost:8000/api/receipts/ 
-> retorna todos as compras do usuário atualmente autenticado

GET http://localhost:8000/api/receipts/<receipt_id>
-> retorna a compra associado a receipt_id

DELETE http://localhost:8000/api/receipts/<receipt_id>
-> retorna todas as compras do usuário atualmente autenticado

Mais detalhes e exemplos de uso nos testes em receipts/tests.py e products/tests.py




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


# **Avaliação:** #

Vamos avaliar seguindo os seguintes critérios:

1. Você conseguiu concluir os requisitos?
2. Você documentou a maneira de configurar o ambiente e rodar sua aplicação?
