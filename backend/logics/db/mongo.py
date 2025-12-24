from pymongo import MongoClient
import os 
from logics.utils.env_loader import load_env
import dns.resolver
import logging

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8','1.1.1.1']

load_env()
logger = logging.getLogger(__name__)
uri = os.getenv("mongo_uri")


_client = None
_db_cache = {}
_indexes_created = False

def get_db_handle(db_name):
   
    global _client, _indexes_created

    if _client is None:
        _client = MongoClient(uri)

    if db_name not in _db_cache:
        _db_cache[db_name] = _client[db_name]

    if not _indexes_created:
        ensure_indexes(_db_cache[db_name])
        _indexes_created = True

    return _db_cache[db_name], _client

def ensure_indexes(db):
    try:
        user_db = db["user_db"]
        qa_pairs= db["qa_pairs"]

        user_db.create_index(
            [("candidate_mail", 1), ("created_at", -1)],
            background=True
        )
        user_db.create_index(
            [("session_id", 1), ("candidate_id", 1)],
            background=True
        )

        qa_pairs.create_index("interviewer_id", background=True)
        qa_pairs.create_index("session_id", background=True)
        qa_pairs.create_index("allowed_candidates", background=True)
        
        logger.info("Mongo indexes ensured")
    except Exception:
        logger.exception("Mongo index creation failed")


