import os
try: 
    import sqlite3
except:
    os.system('pip3 install sqlite3')
    import sqlite3
    
try:
    from pymongo import MongoClient
except:
    os.system('pip3 install pymongo')
    from pymongo import MongoClient
"""
This try/except is for if there is no lib, 
download it and use it in the code
"""

class MongoDb():
    """
    This Connect to Mongo DB
    The functions of this class are
    
    - insert_one (data)
        This function needs a one dict
        example:
        {
            'name':'Jhon Wesley',
            'age':19
        }
    
    - find_one (data)
        This function need a query for find one and first element
        example:
        {
            'age':19
        }  
    
    - find_all(query)
        This function is similar to find_one, but return one list with 
        all elements to query. If the query is not specified, 
        the return will be all items.

        example:
        {
            'name': {
                '$ne' : 'Jhon Wesley'
            }
        }
        
    - update_one(query,set_update)
        This function needs two parameters, one query and the other update.
        The query find one item for update, updates one item at a time
        
        example:
        query = {
            'name':'Jhon Wesley',
            'age':19
        }
        update = {
            'age':25
        }
    
    - find_and_delete(data)
        This function delete one item.
        I haven't created the delete function yet.
    
    """
    
    
    def __init__(self,host:str="mongodb://localhost:27017/",set_dataBase:str="defaultDB",collection:str="userCollection"):
        self.client = MongoClient(host)
        self.db = self.client[set_dataBase]
        self.conector = self.db[collection]
        #db.<colection>.<comando>
    
    def insert_one(self, query):
        self.conector.insert_one(query)
    
    def find_all(self,query=None):
        if query == None:
            return [row for row in self.conector.find()]
        else:
            return [row for row in self.conector.find(query)]
    
    def find_one(self,query:dict):
        
        return self.conector.find_one(query)
    
    def update_one(self,query,set_update):
        self.conector.find_one_and_update(query,{"$set":set_update})
    
    def find_and_delete(self,query:dict):
        self.conector.find_one_and_delete(query)
        
class SqliteDb():
    def __init__(self,path:str="data/dataBase.db"):
        self.db = path
    
    def _connect(self):
        conector = sqlite3.connect(self.db)
        cursor = conector.cursor()
        return conector,cursor
    
    def _creatTable(self):
        conector,cursor = self._connect()
        
        table="""
        CREATE TABLE IF NOT EXISTS candidato (
            cpf NOT NULL PRIMARY KEY,
            nome VARCHAR NOT NULL,
            nota FLOAT NOT NULL,
            id_input VARCHAR NOT NULL
        )
        """
        cursor.execute(table)
    
    def insert_one(self,cpf,nome,nota,id_input):
        conector,cursor = self._connect()
        self._creatTable()
        
        sql = f"""
        INSERT INTO candidato (cpf,nome,nota,id_input)
        VALUES ('{cpf}','{nome}','{nota}','{id_input}')
        """
        
        cursor.execute(sql)
        conector.commit()
        conector.close()
    
    def find_all(self,table:str,column:str='*'):
        conector,cursor = self._connect()
        sql=f"""
        SELECT {column}
        FROM {table}
        """
        cursor.execute(sql)
        return cursor.fetchall()
    
    def find_one(self,table:str,column:str='*',field:str='cpf',index:str='58127043680'):
        conector,cursor = self._connect()
        sql=f"""
        SELECT {column}
        FROM {table}
        WHERE {field} = '{index}'
        """
        cursor.execute(sql)
        return cursor.fetchall()
    
    
    def update_one(self,data):
        pass
    
    def find_and_delete(self,data):
        pass