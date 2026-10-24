"""
Database package init.
"""
from .mongodb import get_db, get_mongo_client, check_connection
from .indexes import create_database_indexes

__all__ = ["get_db", "get_mongo_client", "check_connection", "create_database_indexes"]
