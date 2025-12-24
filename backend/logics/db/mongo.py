from pymongo import MongoClient
import os 
from logics.utils.env_loader import load_env
import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8','1.1.1.1']

load_env()

uri = os.getenv("mongo_uri")


_client = None

def get_client():
    global _client
    if _client is None:
        _client= MongoClient(uri)
    return _client

def ensure_indexes(db):
    user_db = db["user_db"]
    qa_pairs= db["qa_pairs"]

    user_db.create_index("candidate_mail")
    user_db.create_index("session_id")
    user_db.create_index([("session_id", 1), ("candidate_mail", 1)], background=True)

    qa_pairs.create_index("interviewer_id")
    qa_pairs.create_index("session_id")
    qa_pairs.create_index("allowed_candidates")

def get_db_handle(db_name):
    client = get_client()
    db=client[db_name]
    ensure_indexes(db)
    
    return db, client

