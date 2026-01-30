"""
Diagnostic script to query the database for captured threats.
"""
import sqlite3
import os

DB_PATH = os.path.join("data", "threats.db")


def check_database():
    """Queries the database and prints all captured threats."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM threats")
        rows = cursor.fetchall()
        
        print(f"\nTotal Capture Count: {len(rows)}")
        print("-" * 50)
        
        for row in rows:
            print(f"Threat Record: {row}")

        conn.close()

    except Exception:
        print("Database is empty, locked, or inaccessible.")


if __name__ == "__main__":
    check_database()