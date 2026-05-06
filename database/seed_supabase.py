from database.connection import get_db
from core.security import hash_password
import uuid

def seed_supabase():
    db = get_db()
    if not db:
        print("❌ Supabase client not initialized. Check your .env file.")
        return

    print("🚀 Seeding Supabase database...")

    try:
        # 1. Create AI User
        ai_user = {
            "id": str(uuid.uuid4()),
            "email": "ai@mindloop.io",
            "username": "MindLoop_AI",
            "full_name": "MindLoop Artificial Intelligence",
            "password_hash": "SYSTEM_ACCOUNT"
        }
        
        # Check if already exists
        res = db.table("users").select("*").eq("email", "ai@mindloop.io").execute()
        if not res.data:
            db.table("users").insert(ai_user).execute()
            print("✅ AI User created.")
        else:
            print("ℹ️ AI User already exists.")

        # 2. Create Demo User
        demo_pwd = hash_password('password123')
        demo_user = {
            "id": str(uuid.uuid4()),
            "email": "demo@mindloop.io",
            "username": "MasterMind",
            "full_name": "Master Mind",
            "password_hash": demo_pwd
        }
        
        res = db.table("users").select("*").eq("email", "demo@mindloop.io").execute()
        if not res.data:
            db.table("users").insert(demo_user).execute()
            print("✅ Demo User created.")
        else:
            print("ℹ️ Demo User already exists.")

        print("✨ Seeding completed successfully!")

    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")

if __name__ == "__main__":
    seed_supabase()
