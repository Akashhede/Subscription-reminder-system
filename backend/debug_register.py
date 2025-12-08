from backend.database import SessionLocal
from backend import crud, schemas
import traceback

def debug_register():
    db = SessionLocal()
    try:
        print("Attempting to create user...")
        user = crud.create_user(db, "debug_user@example.com", "password", "1234567890")
        print("User created:", user.id)
    except Exception:
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_register()
