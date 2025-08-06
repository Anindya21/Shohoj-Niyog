from pymongo import MongoClient
import os 
from utils.env_loader import load_env
import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8','1.1.1.1']

load_env()

uri = os.getenv("mongo_uri")

def get_db_handle(db_name):
    client = MongoClient(uri)
    db_handle = client[db_name]
    return db_handle, client

