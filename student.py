import re
from unicodedata import normalize
from anyFunction import valeusNotNull

def generateResponses (status, message, name_content=False,content=False):
    response = {}
    response["status"] = status
    response["message"]= message

    if name_content and content:
        response[name_content] = content

    return response,status


def validateCpf(cpf):
    if len(cpf) >= 11:
        cpf = "".join(re.findall("[0-9]",cpf))
        if len(cpf) != 11:
            return {
                "status_code":422,
                "message":f"The CPF is invalid '{cpf}'. The CPF number must contain 11 digits"
        },False
            
        else:
            return cpf,True
    
    else:
        return {
                "status_code":422,
                "message":f"The CPF is invalid '{cpf}'. The CPF number must contain 11 digits"
        },False    
        
        
def validateStudent(data):
    """-------NOT NULL FILTER------"""
    check_notnull=valeusNotNull(data)
    if not check_notnull[1]:
        return check_notnull[0],False,400
    
    else:
        """-------NAME FILTER--------"""
        try:
            data['name']= data['name'].strip()
        
        except:
            pass
        
        else:
            if len(data['name'].split(' ')) > 1:      
                data['name'] = normalize('NFKD', data['name']).encode('ASCII','ignore').decode('ASCII').upper() #remove special characters ´`ç~ªº and capitalize the name 
                
            else:
                return {
                        "status_code":422,
                        "message":f"The name is invalid '{data['name']}'. I need name and surname"
                },False
                
        """------CPF FILTER----------"""        
        try:
            cpf=validateCpf(data['cpf'])

        except:
            pass
        
        else:
            if not cpf[1]:
                return cpf[0],False
            
            else:
                data["cpf"] = cpf[0]  
                        
        """-------PHONE FILTER-------"""
        try:
            phone_number = data["phone"]
        
        except:
            pass
        
        else:        
            if len(phone_number) > 11:
                phone_number = re.sub(r"[.,#)+( -]", "", phone_number) #remove caracters or re.findall(...) get only numbers
            
            elif len(phone_number) < 11:
                return {
                        "status_code":422,
                        "message":f"The number phone is invalid '{phone_number}'. The phone number must contain 11 digits. Example: 10 9 8765 4321"
                },False
            
            else:
                phone_number = "".join(re.findall("[0-9]",phone_number)) #get only numbers in phone_number with re.findall(), the return is list. 
            
            if len(phone_number) != 11:
                return {
                        "status_code":422,
                        "message":f"The number phone is invalid '{phone_number}'. The phone number must contain 11 digits. Example: 10 9 8765 4321"
                },False
                
            else:
                data["phone"] = phone_number
                """
                O retorno do telefone deve ser igual a 11 digitos. Qualquer valor diferente deve
                retornar um erro e pedir para que insira um numero válido. 
                """
            
            """------END PHONE FILTER--------"""   
        
        return data,True    
