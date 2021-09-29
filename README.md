# apiTest

#Instrução
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

#Como usar
Use os endpoints abaixo para cadastrar, atualizar e listar alunos:
 - `/register/student` methods = "POST","PUT" -> Cadastrar
 - `/update/student/<user>` methods = "POST","PUT" -> Atualizar
 - `/update/student` methods = "GET" -> Listar

Para usar só é permitido dados no formato JSON, exemplo permitido ao criar/atualizar um aluno:
    {
        'name':'Jhonny Jhonson',
        'cpf':'12345678909',
        'nickname':'JhonJhon',
        'phone':'48911112222',
        'avatar':'avatar'
    }

Use os endpoints abaixo para cadastrar, atualizar, listar e excluir curso:
 - `/register/course` methods = "POST","PUT" -> Cadastrar
 - `/update/course/<id>` methods = "POST","PUT" -> Atualizar
 - `/update/course` methods = "GET" -> Listar
 - `/del/course/<id>` methods = "DELETE" -> excluir

Exemplo permitido para criar/atualizar um curso:
    {  
        'name':'psicologia',
        'description':'O curso contém informações sobre...',
        'holder_image':'image',
        'duration':2220
    }

#Observações
Algumas funções da primeira etapa do teste não está concluida. Isso será alterado posteriormente ao sofrer 
as novas atualizações.
Alguns endpoints mencionados não conclui até o momento, exemplos: deletar/listar curso e listar alunos.
Não usei nenhum mecanismo para tratamento de imagem, não testei isso e não se pode falhar a API devido a isso.
Como ainda não possuo conhecimentos técnicos para lidar com imagens, vou realizar mecanismos para lidar com isso
ao final da primeira etapa.
Também criei uma senha para 'possuir segurança' na API, no caso, necessário inserir no header a senha `{"Authorization":"aaabbccc123"}`
Isso pode ser desnecessário dependendo do esquema de négocio, por exemplo, se User não tiver permissão para excluir
curso, mas, possui acesso ao criar/listar isso seria bem interessante bloquear o User para não excluir informações. 
Caso o user saiba o que está fazendo e possui acesso a tudo é descenessário essa aplicação.
O funcionamento dessa aplicação é bem simples. Ocorre uma busca no DB pela senha, caso não encontre a senha, o 
usuario não tem permissão para acessar a aplicação. Se a senha for encontrada no DB, será verificado no schema
se aquele usuario possui acesso a tal função, por exemplo: deletar, atualizar, cadastrar, etc. 
Caso não possua permissão o retorno deve ser usuário sem permissão (User unauthorized).
