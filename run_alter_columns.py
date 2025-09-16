from supabase import create_client

SUPABASE_URL = "https://nhcevgvrdjzcazlmzrft.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oY2V2Z3ZyZGp6Y2F6bG16cmZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5NzA0OTYsImV4cCI6MjA3MzU0NjQ5Nn0.mwCUjtW16I7PKKPbSLpZK7JhgqIJDvr7KWiCkTQhAMk"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def run_alter_table():
    sql = """
    ALTER TABLE profiles ADD COLUMN IF NOT EXISTS email TEXT;
    ALTER TABLE profiles ADD COLUMN IF NOT EXISTS name TEXT;
    ALTER TABLE user_saved_internships DROP CONSTRAINT IF EXISTS user_saved_internships_user_id_fkey;
    ALTER TABLE user_applied_internships DROP CONSTRAINT IF EXISTS user_applied_internships_user_id_fkey;
    """
    response = supabase.rpc("sql", {"q": sql}).execute()
    if response.get("error"):
        print("Error running ALTER TABLE:", response.get("error"))
    else:
        print("ALTER TABLE commands executed successfully.")

if __name__ == "__main__":
    run_alter_table()
