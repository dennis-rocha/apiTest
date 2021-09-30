"""
Mensagem de Boas Vindas!

Bem vind@!

Em algumas partes do código o retorno da função será uma TUPLA
Para melhor compreender o que se passa dentro do código e por default
adaptei para que o retorno no index 0 seje o dado para trabalhar e 
Index 1 é True ou False. Caso index 1 for Falso o dado (index 0) 
Provavelmente será um dicionario contento status_code e message do erro
E caso seje True no nosso index 1 terá uma certa sequencia normal a se 
Manipular com os dados o qual estará no index 0  

 

"""
import re
from os import name
from flask import Flask, request
from datetime import datetime
from unicodedata import normalize
from student import generateResponses, validateCpf, validateStudent
from course import validateCourse
from anyFunction import valeusNotNull, checkHeader
from saveData import MongoDb

app = Flask("apiTest")

@app.route("/hi", methods=["GET"])
def teste ():
    return {'message':'Hello World'}


# Cadastrar novos alunos
@app.route("/register/student", methods=["POST","PUT"])
def addStudent():
    header=request.headers.get("Authorization")
    students_keys = ['name', 'cpf', 'nickname', 'phone','avatar']
    try:        
        body = request.get_json(force=True)
    except:
        return generateResponses(400, 'I need a valid JSON in the request body')
    
    autho = checkHeader(header)#return is Tuple 
    
    if not autho[1]:
        return generateResponses(autho['status_code'],autho['message'])
    else:
        
        
        for key in students_keys: ##check 'body' has all keys
            if key not in body.keys():
                return generateResponses(400,                                              
                                         f"I need see '{key}' in body", 
                                         'example_permited',
                                         {  
                                             'name':'Jhonny Jhonson',
                                             'cpf':'12345678909',
                                             'nickname':'JhonJhon',
                                             'phone':'48911112222',
                                             'avatar':'avatar'
                                         }
                )
        for key in body.keys(): #check if 'body' has too many keys or not equal the example
            if key not in students_keys:
                return generateResponses(400,                                              
                                         f"The key '{key}' cannot create students", 
                                         'example_permited',
                                         {
                                             'name':'Jhonny Jhonson',
                                             'cpf':'12345678909',
                                             'nickname':'JhonJhon',
                                             'phone':'48911112222',
                                             'avatar':'avatar'
                                         }
                )
        
        data = validateStudent(body)
        if not data[1]:
            return generateResponses(data[0]['status_code'],data[0]['message'])
        
        else:
            db = MongoDb(set_dataBase="apiTest",collection="student") #db conection, collection student for student
            data=data[0]
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data['date_created'] = date
            data['date_updated'] = date
            data['_id'] = len(db.find_all())+1
            db.insert_one(data)
            
            return generateResponses(201,"User registration success", "student", data)
                
                    
# Editar novos alunos
@app.route("/update/student/<user>", methods=["POST","PUT"])
def updateStudent(user=None):
    header=request.headers.get("Authorization")
    try:        
        body = request.get_json(force=True)
    except:
        return generateResponses(400, 'I need a valid JSON in the request body')
    
    students_keys = ['name', 'cpf','nickname', 'phone', 'avatar']            
    autho = checkHeader(header)
    
    if not autho[1]:
        return generateResponses(autho['status_code'],autho['message']),autho[2]
    
    else:
        if not user:
            return generateResponses(400, "Please, insert student key 'CPF' for update")
        
        else:
            for key in body.keys():
                if not key in students_keys:
                    return generateResponses(400, f"The key '{key}' cannot update student")
            
            cpf = validateCpf(user)
            if not cpf[1]:
                return generateResponses(cpf[0]["status_code"], cpf[0]["message"])
            
            else:
                cpf = cpf[0]
                
            body = validateStudent(body)    
            if not body[1]:
                return generateResponses(body[0]['status_code'],body[0]['message'])
            
            else:
                body=body[0]
                db = MongoDb(set_dataBase="apiTest",collection="student")
                data = db.find_one({"cpf":cpf})#Pesquisar pelo CPF
                if not data:
                    return generateResponses(404, f"User CPF '{cpf}' Not Found")
                
                else:
                    body['date_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    try:
                        db.update_one({"cpf":cpf},body)
                    
                    except Exception as error:
                        return generateResponses(500, f"Internal Error:\n{error}")
                    
                    else:
                        return generateResponses(201, f"Student update success")

                    
# Cadastrar novos cursos
@app.route("/register/course", methods=["POST"])
def registerCourse():
    header=request.headers.get("Authorization")
    try:        
        body = request.get_json(force=True)
    except:
        return generateResponses(400, 'I need a valid JSON in the request body')
    
    course_keys = ["name", "description", "holder_image", "duration"]            
    autho = checkHeader(header)
    
    if not autho[1]:
        return generateResponses(autho['status_code'],autho['message']),autho[2]
    
    else:
        for key in course_keys: ##check 'body' has all keys
            if key not in body.keys():
                return generateResponses(400,                                              
                                         f"I need see '{key}' in body", 
                                         'example_permited',
                                         {  
                                             'name':'psicologia',
                                             'description':'O curso contém informações sobre...',
                                             'holder_image':'image',
                                             'duration':2220
                                         }
                )
                
        for key in body.keys(): #check if 'body' has too many keys or not equal the example
            if key not in course_keys:
                return generateResponses(400,                                              
                                         f"The key '{key}' cannot create students", 
                                         'example_permited',
                                         {  
                                             'name':'psicologia',
                                             'description':'O curso contém informações sobre...',
                                             'holder_image':'image',
                                             'duration':2220
                                         }
                )
        if not valeusNotNull(body)[1]:
            data = valeusNotNull(body)[0]
            return generateResponses(data["status_code"], data["message"])
        
        else:            
            data = validateCourse(body)
            if not data[1]:
                return generateResponses(data[0]["status_code"], data[0]["message"])
            
            else:
                data=data[0]
                db = MongoDb(set_dataBase="apiTest",collection="course")
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(data)
                data['date_created'] = date
                data['date_updated'] = date
                data['_id'] = len(db.find_all())+1
                db.insert_one(data)
            
                return generateResponses(201,"User registration success", "student", data)
            

#Atualizar novo cursos
@app.route("/update/course/<course>", methods=["POST","PUT"])
def updateCourse(course):
    header=request.headers.get("Authorization")
    try:        
        body = request.get_json(force=True)
    except:
        return generateResponses(400, 'I need a valid JSON in the request body')
    
    course_keys = ["name", "description", "holder_image", "duration"]            
    autho = checkHeader(header)
    
    if not autho[1]:
        return generateResponses(autho['status_code'],autho['message']),autho[2]
    
    else:
        if not course:
            return generateResponses(400, "Please, insert course key '_id' for update")
        else:
            db = MongoDb(set_dataBase="apiTest",collection="course")
            print(course)
            data = db.find_one({"_id":int(course)})
            print(data)
            if not data:
                return generateResponses(404, f"Course key '{course}' Not Found")
            else:
                for key in body.keys():
                    if not key in course_keys:
                        return generateResponses(400, f"The key '{key}' cannot update course")
                
                if not valeusNotNull(body)[1]:
                    data = valeusNotNull(body)[0]
                    return generateResponses(data["status_code"], data["message"])
        
                body = validateCourse(body)
                if not body[1]:
                    return generateResponses(body[0]['status_code'],body[0]['message'])
                else:
                    body=body[0]
                    body['date_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    try:
                        print(body)
                        db.update_one({"_id":int(course)},body)
                    
                    except Exception as error:
                        return generateResponses(500, f"Connot save,Internal Error:\n{error}")
                    
                    else:
                        return generateResponses(201, f"Course update success")


# Listar todos os cursos do catalogo
@app.route("/read/course", methods=["GET"])
def readCourse ():
    db = MongoDb(set_dataBase="apiTest",collection="course")
    data = db.find_all()
    print(data)
    if not data:
        return generateResponses(200, "No have data to show here")
    else:
        return generateResponses(200, "Data found successfully", "data",data)

# Listar todos os alunos
@app.route("/read/student", methods=["GET"])
def readStudent ():
    db = MongoDb(set_dataBase="apiTest",collection="student")
    data = db.find_all()
    for row in data:
        row["_id"] = str(row["_id"])
    
    if not data:
        return generateResponses(200, "No have data to show here")
    else:
        return generateResponses(200, "Data found successfully", "data",data)


"""
# Matricular um aluno em um curso
@app.route("/oi", methods=["GET"])
def teste ():
    pass



# Excluir cursos existentes
@app.route("/oi", methods=["GET"])
def teste ():
    pass


# Remover o aluno de um curso

@app.route("/oi", methods=["GET"])
def teste ():
    pass
"""

app.run()