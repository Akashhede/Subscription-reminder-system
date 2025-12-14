"""
Migration script to add start_date column to subscriptions table.
Run this once to update existing database schema.
"""
import sqlite3
import os

# Get database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "subscriptions.db")

def migrate():
    """Add start_date column to subscriptions table if it doesn't exist"""
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. It will be created when you run the app.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(subscriptions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'start_date' not in columns:
            print("Adding start_date column to subscriptions table...")
            cursor.execute("ALTER TABLE subscriptions ADD COLUMN start_date DATE")
            conn.commit()
            print("✅ Migration successful: start_date column added")
        else:
            print("✅ start_date column already exists, skipping migration")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()



