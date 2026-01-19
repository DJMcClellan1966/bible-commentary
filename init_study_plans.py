"""
Initialize default study plans in the database
"""
from models import init_db, SessionLocal
from study_plans import initialize_default_plans

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    
    print("\nCreating default study plans...")
    db = SessionLocal()
    try:
        plans = initialize_default_plans(db)
        print(f"\n✓ Created {len(plans)} study plans")
        print("\nDefault plans available:")
        print("  - Bible in a Year")
        print("  - Psalms & Proverbs in a Month")
        print("  - New Testament in 90 Days")
        print("  - 30 Days in the Gospels")
    finally:
        db.close()
