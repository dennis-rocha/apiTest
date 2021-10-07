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
            del data["enrollment_course"]
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
                (data)
                data["active_course"]=False
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
    
    course_keys = ["name", "description", "holder_image", "duration", "active_course"]            
    autho = checkHeader(header)
    
    if not autho[1]:
        return generateResponses(autho['status_code'],autho['message']),autho[2]
    
    else:
        if not course:
            return generateResponses(400, "Please, insert course key '_id' for update")
        else:
            db = MongoDb(set_dataBase="apiTest",collection="course")
            
            data = db.find_one({"_id":int(course)})
            
            if not data:
                return generateResponses(404, f"Course key '{course}' Not Found")
            else:
                for key in body.keys():
                    if not key in course_keys:
                        return generateResponses(400, f"The key '{key}' cannot update course")
                
                if not valeusNotNull(body)[1]:
                    data = valeusNotNull(body)[0]
                    return generateResponses(data["status_code"], data["message"])
                
                if type(body["active_course"]) != bool:
                    return generateResponses(422, "Please, insert type Bool (True or False) for update in key 'active_course'")
                
                body = validateCourse(body)
                if not body[1]:
                    return generateResponses(body[0]['status_code'],body[0]['message'])
                else:
                    body=body[0]
                    body['date_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    try:
                        
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


# Matricular um aluno em um curso
@app.route("/enroll/course/<id_course>/student/<cpf>", methods=["GET"])
def enrollment(id_course,cpf):
    db_student = MongoDb(set_dataBase="apiTest",collection="student")
    data_student = db_student.find_one({"cpf":cpf})
    
    if not data_student:
        return generateResponses(422, f"This cpf {cpf} was not found")
    
    else:
        db_course = MongoDb(set_dataBase="apiTest",collection="course")
        data_course = db_course.find_one({"_id":int(id_course)})
        if not data_course:
            return generateResponses(422, f"This course {id_course} was not found")
        
        else:           
            data = {
                "student":cpf,
                "date_enroll":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "date_close":"",
                "score":0,
                "status":"andamento"        
            }
                  
            try:
                enroll = db_course.find_one({"_id":int(id_course)})["enrollment_course"]
                
            except:
                enroll = []
            
            finally:
                for row in enroll:
                    if cpf in row["student"]:
                        return generateResponses(200, f"This CPF {cpf} already has in the course informed")
                
                data["id"] = len(enroll)+1
                enroll.append(data)
        
            try:              
                db_course.update_one({"_id":int(id_course)},{"active_course":True,"enrollment_course":enroll})
            
            except:
                return generateResponses(500, f"An internal error has occurred and cannot be created")
            
            else:                    
                
                return generateResponses(201, f"Student enrollment was successful.","enrollment_create",data)
            

# Atualizar matricula do aluno
@app.route("/update/enrollment/<id_course>/student/<cpf>", methods=["POST","PUT"])
def updateEnrollment(id_course,cpf):
    db_student = MongoDb(set_dataBase="apiTest",collection="student")
    data_student = db_student.find_one({"cpf":cpf})
    enroll_keys = ["score", "status"]
    try:        
        body = request.get_json(force=True)
    except:
        return generateResponses(400, 'I need a valid JSON in the request body')
    
    if not data_student:
        return generateResponses(422, f"This cpf {cpf} was not found")
    
    else:
        db_course = MongoDb(set_dataBase="apiTest",collection="course")
        data_course = db_course.find_one({"_id":int(id_course)})
        if not data_course:
            return generateResponses(422, f"This course {id_course} was not found")
        
        else:
            for key in enroll_keys:
                if key not in body.keys():
                    return generateResponses(400, f"I need see '{key}' in body")
            
            for key in body.keys():
                if key not in enroll_keys:
                    return generateResponses(400, f"The key '{key}' cannot update enrollment")
                
            try:
                if type(body["score"]) == float or type(body["score"]) == int:
                    if body["score"] < 0 or body["score"] > 10:
                        return generateResponses(400, f"The key 'score' need values ​​between 0 and 10")
                    
                    else:
                        score = body["score"]
                
                else:    
                    score = float( #Rransform string in type float
                        "".join( #re.findall return list, this join concatenate all number and . in the list
                            re.findall(
                                "[0-9.-]", #Regex for get numbers and .
                                body["score"] #Variable to perform the regex
                            )
                        )
                    )
                    
                    if score < 0 or score > 10:
                        return generateResponses(400, f"The key 'score' need values ​​between 0 and 10")
                    
            except:
                return generateResponses(400, f"The key 'score' needs type float")
            
            else:
                body["score"] = score
                
            status_enroll = ["aprovado", "reprovado", "andamento"]
            if body["status"] not in status_enroll:   
                return generateResponses(400, f"The value in key 'status' cannot update enrollment","example_permited",{1:"andamento",2:"reprovado",3:"aprovado"})
            
            else:
                status_course = False
                for row in data_course["enrollment_course"]:
                    if row["student"] == cpf:
                        row["score"] = body["score"]
                        row["status"] = body["status"]
                        row["date_close"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        status_course = True
                if not status_course:
                    return generateResponses(422, f"This cpf {cpf} was not found")
                
                else:
                    try:       
                        db_course.update_one({"_id":int(id_course)},data_course)
                    
                    except:
                        return generateResponses(500, f"An internal error has occurred and cannot be update")
                    
                    else:
                        return generateResponses(201, f"Course update success")

                    


# Remover o aluno de um curso
@app.route("/unenroll/course/<id_course>/student/<cpf>", methods=["DELETE"])
def unenrollment(id_course,cpf):
    db_student = MongoDb(set_dataBase="apiTest",collection="student")
    data_student = db_student.find_one({"cpf":cpf})
    
    if not data_student:
        return generateResponses(422, f"This cpf {cpf} was not found")
    
    else:
        db_course = MongoDb(set_dataBase="apiTest",collection="course")
        data_course = db_course.find_one({"_id":int(id_course)})
        if not data_course:
            return generateResponses(422, f"This course {id_course} was not found")
        
        else: 
            try:
                enroll = db_course.find_one({"_id":int(id_course)})["enrollment_course"]
                
            except:
                enroll = []
            
            finally:
                if not enroll:
                    return generateResponses(422, "This course has no student enrolled")
                
                else:
                    for row in enroll:
                        if cpf not in row["student"]:
                            return generateResponses(400, f"This CPF {cpf} not in the course informed")
                        
                        else:
                            data = enroll.pop(enroll.index(row))
                    
                    try:              
                        db_course.update_one({"_id":int(id_course)},{"enrollment_course":enroll})
            
                    except:
                        return generateResponses(500, f"An internal error has occurred and cannot be remove")
                    
                    else:                                           
                        return generateResponses(200, f"Student's enrollment cancellation was successful","student_removed",data)
                    
                        
#Excluir cursos existentes
@app.route("/delete/course/<id_course>", methods=["DELETE"])
def deleteCourse(id_course):
    db = MongoDb(set_dataBase="apiTest",collection="course")
    data = db.find_one({"_id":int(id_course)})
    if not data:
        return generateResponses(422, f"This course {id_course} was not found")
    
    else:
        if data["active_course"]:
            return generateResponses(422, "This course is active, you need to deactivate it first to delete it. Go update and try again")
            
        else:
            try:
                db.find_and_delete({"_id":int(id_course)})
                
            except:
                return generateResponses(500, f"An internal error has occurred and cannot be remove")
            
            else:
                return generateResponses(200, f"Course deleted successfully", "course_deleted", data)

app.run()