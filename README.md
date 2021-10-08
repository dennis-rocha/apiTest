# apiTest

# Instrução

Para usar esse teste você deve possuir na sua máquina instalado algumas libs, são elas: `Flask, pymongo, sqlite3`
Caso você não possua essas libs, elas serão baixadas automaticamente na primeira execução.
Você também deve conter o mongo instalado na sua máquina e com o servidor ligado. Você pode testar
se o mongo está funcionando usando o terminal do seu SO, use o comando `mongo`, se mudar para o shell do mongo
ao executar o comando o teste não haverá falhas ao usar o Banco de Dados. O destino para acessar o mongo está como
localhost:27017 (porta padrão), você pode alterar isso no arquivo saveData.py e inserir o local/porta que desejar ou
pode alterar isso direto no código na chamada da função `MongoDb(host:str="mongodb://localhost:27017/",set_dataBase:str="defaultDB",collection:str="userCollection")`. No entanto é mais pratico alterar apenas uma vez
com a primeira opção.
O desafio consiste em criar API's para soluções de e-learning, mais detalhes no arquivo teste.txt.
O desafio deve conter API's para:

- Cadastrar/atualizar Aluno e listar todos os alunos
- Cadastrar/atualizar Curso, listar todos os cursos e excluir cursos
- Matricular/remover aluno em um curso

<br>

# Como usar

Para usar as APIs para criar ou atualizar só é permitido dados no formato JSON no body, segue abaixo os exemplos permitidos para criar/atualizar um aluno:

    {
        'name':'Jhonny Jhonson',
        'cpf':'12345678909',
        'nickname':'JhonJhon',
        'phone':'48911112222',
        'avatar':'avatar'
    }

Exemplo permitido para criar/atualizar um curso:

    {  
        'name':'psicologia',
        'description':'O curso contém informações sobre...',
        'holder_image':'image',
        'duration':2220
    }

Use os endpoints abaixo para cadastrar, atualizar e listar alunos:

- `/register/student` methods = "POST","PUT" -> Cadastrar
- `/update/student/<user>` methods = "POST","PUT" -> Atualizar
- `/update/student` methods = "GET" -> Listar

Use os endpoints abaixo para cadastrar, atualizar, listar e excluir curso:

- `/register/course` methods = "POST","PUT" -> Cadastrar
- `/update/course/<id>` methods = "POST","PUT" -> Atualizar
- `/update/course` methods = "GET" -> Listar
- `/del/course/<id>` methods = "DELETE" -> excluir

Use os endpoints abaixo para matricular aluno no curso, remover matrícula e atualizar matrícula do curso

- `/enroll/course/<id_course>/student/<cpf>` methods = "GET" -> Matricular aluno
- `/unenroll/course/<id_course>/student/<cpf>` methods = "DELETE" -> Remover matrícula
- `/update/enrollment/<id_course>/student/<cpf>` methods = "POST", "PUT" -> Atualizar matrícula

# Observações

Não usei nenhum mecanismo para tratamento de imagem, não testei isso e não se pode falhar a API devido a isso.
Como ainda não possuo conhecimentos técnicos para lidar com imagens, vou realizar mecanismos para lidar com isso na proxima atualização.

Também criei uma senha para alguns endpoints `{"Authorization":"aaabbccc123"}`
Vou excluir essa funcionalidade na proxima atualização.
