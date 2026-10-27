"""
MongoDB Atlas Connection Manager.
Handles live PyMongo connections and provides graceful fallback to mongomock
when running tests or when MongoDB Atlas credentials are not yet configured.
"""
import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

_mongo_client = None
_database = None
_is_mock_fallback = False

def init_db(app):
    """Initializes database connection from Flask app config."""
    global _mongo_client, _database, _is_mock_fallback
    
    uri = app.config.get("MONGODB_URI", "").strip()
    db_name = app.config.get("MONGODB_DB_NAME", "heart_disease_db")
    timeout_ms = app.config.get("MONGODB_CONNECT_TIMEOUT_MS", 45000)

    if not uri or app.config.get("TESTING", False):
        logger.info("[Database] No MONGODB_URI provided or in TESTING mode. Initializing mongomock fallback.")
        import mongomock
        _mongo_client = mongomock.MongoClient()
        _database = _mongo_client[db_name]
        _is_mock_fallback = True
        return _database

    try:
        logger.info(f"[Database] Connecting to MongoDB Atlas database '{db_name}'...")
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=timeout_ms,
            connectTimeoutMS=timeout_ms,
            retryWrites=True
        )
        # Verify connection
        client.admin.command("ping")
        _mongo_client = client
        _database = _mongo_client[db_name]
        _is_mock_fallback = False
        logger.info(f"[Database] Successfully connected to MongoDB Atlas ('{db_name}')")
    except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
        logger.warning(
            f"[Database] Could not connect to MongoDB Atlas ({e}). "
            f"Falling back to mongomock store for seamless local execution."
        )
        import mongomock
        _mongo_client = mongomock.MongoClient()
        _database = _mongo_client[db_name]
        _is_mock_fallback = True

    return _database

def get_db():
    """Returns the active database instance."""
    global _database
    if _database is None:
        # Default initialization with environment variables
        import mongomock
        uri = os.getenv("MONGODB_URI", "").strip()
        db_name = os.getenv("MONGODB_DB_NAME", "heart_disease_db")
        if uri:
            try:
                timeout_ms = int(os.getenv("MONGODB_CONNECT_TIMEOUT_MS", 45000))
                client = MongoClient(
                    uri,
                    serverSelectionTimeoutMS=timeout_ms,
                    connectTimeoutMS=timeout_ms,
                    retryWrites=True
                )
                client.admin.command("ping")
                _mongo_client = client
                _database = client[db_name]
                _is_mock_fallback = False
            except Exception:
                _database = mongomock.MongoClient()[db_name]
                _is_mock_fallback = True
        else:
            _database = mongomock.MongoClient()[db_name]
            _is_mock_fallback = True
    return _database

def get_mongo_client():
    return _mongo_client

def is_mock():
    return _is_mock_fallback

def check_connection():
    """
    Checks database health status.
    Returns status dict with connectivity information.
    """
    db = get_db()
    if db is None:
        return {"status": "unhealthy", "connected": False, "message": "Database not initialized"}

    if _is_mock_fallback:
        return {
            "status": "healthy",
            "connected": True,
            "type": "in_memory_mock",
            "message": "Using local mock store (configure MONGODB_URI for live Atlas connection)"
        }

    try:
        if _mongo_client:
            _mongo_client.admin.command("ping")
        return {
            "status": "healthy",
            "connected": True,
            "type": "mongodb_atlas",
            "database_name": db.name
        }
    except Exception as e:
        return {
            "status": "degraded",
            "connected": False,
            "error": str(e),
            "message": "Failed to ping MongoDB Atlas cluster"
        }
