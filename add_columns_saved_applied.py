from supabase import create_client

SUPABASE_URL = "https://nhcevgvrdjzcazlmzrft.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oY2V2Z3ZyZGp6Y2F6bG16cmZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5NzA0OTYsImV4cCI6MjA3MzU0NjQ5Nn0.mwCUjtW16I7PKKPbSLpZK7JhgqIJDvr7KWiCkTQhAMk"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def add_columns():
    # Add skills and sectors to user_saved_internships
    sql1 = """
    ALTER TABLE user_saved_internships ADD COLUMN IF NOT EXISTS skills TEXT[];
    ALTER TABLE user_saved_internships ADD COLUMN IF NOT EXISTS sectors TEXT[];
    """
    # Add skills and sectors to user_applied_internships
    sql2 = """
    ALTER TABLE user_applied_internships ADD COLUMN IF NOT EXISTS skills TEXT[];
    ALTER TABLE user_applied_internships ADD COLUMN IF NOT EXISTS sectors TEXT[];
    """
    try:
        supabase.rpc("sql", {"q": sql1}).execute()
        print("Added columns to user_saved_internships.")
        supabase.rpc("sql", {"q": sql2}).execute()
        print("Added columns to user_applied_internships.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    add_columns()
