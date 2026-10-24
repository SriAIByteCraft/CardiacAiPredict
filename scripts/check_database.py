"""
Database connectivity verification script.
Runs diagnostics against configured MongoDB Atlas URI or local mock.
"""
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from database.mongodb import check_connection, get_db

def main():
    print("=" * 60)
    print("Heart Disease Prediction System - Database Diagnostic")
    print("=" * 60)
    
    status = check_connection()
    print(f"Connection Status: {status.get('status').upper()}")
    print(f"Connected:         {status.get('connected')}")
    print(f"Backend Store:     {status.get('type')}")
    print(f"Message:           {status.get('message') or status.get('error')}")

    if status.get("connected"):
        db = get_db()
        users_count = db.users.count_documents({})
        preds_count = db.predictions.count_documents({})
        print(f"Users Count:       {users_count}")
        print(f"Predictions Count: {preds_count}")
        print("=" * 60)
        print("Database is ready.")
        sys.exit(0)
    else:
        print("=" * 60)
        print("Database connection failed. Please check MONGODB_URI in backend/.env.")
        sys.exit(1)

if __name__ == "__main__":
    main()
