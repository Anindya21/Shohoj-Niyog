from pymongo import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv()

username= os.getenv("mongo_user")
password= os.getenv("mongo_pass")
host= os.getenv("host")
port = os.getenv("port") 

def get_db_handle(db_name, host, port, username, password):

    client = MongoClient(host=host,
                      port=int(port),
                      username=username,
                      password=password
                     )
    db_handle = client['interview_db']
    
    return db_handle, client