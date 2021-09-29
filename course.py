
import re
from unicodedata import name


def validateCourse(data):
    """-------NAME FILTER-------"""
    try:
        data["name"] = data["name"].strip().upper()
    
    except:
        pass
    

    """-------DESCRIPTION FILTER-------"""
    try:
        data["description"] = data["description"].strip()
    
    except:
        if data["description"] != str:
            return {
                "status_code":400,
                "message":"The description needs text"
            },False
    
    else:
        if len(data["description"]) < 10:
            return {
                "status_code":422,
                "message":"The description is very small, need description > 10"    
            }, False
            
    """-------DURATION FILTER-------"""
    try:
        duration="".join(re.findall("[0-9]",data['duration']))
    
    except:
        pass
    
    else:
        if not duration:
            return {
                "status_code":400,
                "message":"The key 'duration' needs int numbers"
            },False
        
        else:
            data["duration"] = int(duration)
            
            if data["duration"] < 1:
                return {
                    "status_code":422,
                    "message":"The duration of course not accept, insert int numbers > 0"
                }
            
    return data,True