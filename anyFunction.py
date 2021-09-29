

def valeusNotNull(data):
    for k,v in data.items():
        if not v:
            return {
                "status_code":400,
                "message":f"The key '{k}' Not Null"
            },False
    return data,True

def checkHeader(header=None,methods=None):
    passcode = 'aaabbccc123'
    autho = True
    if header == passcode:
        if autho: 
            return autho,True
        
        else:
            {"message":"User unauthorized","code":401},False,401
            
    else:
        return {"message":"User unauthenticated","code":403},False,403

