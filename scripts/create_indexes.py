"""
Database index creation script.
Creates unique index on email, compound indexes on user_id and timestamps.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from database.mongodb import get_db
from database.indexes import create_database_indexes

def main():
    print("=" * 60)
    print("Heart Disease Prediction System - Database Indexes Initialization")
    print("=" * 60)
    db = get_db()
    res = create_database_indexes(db)
    print(f"Index creation results: {res}")
    print("Completed ensuring database indexes.")
    print("=" * 60)

if __name__ == "__main__":
    main()
