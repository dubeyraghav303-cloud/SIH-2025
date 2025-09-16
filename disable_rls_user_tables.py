from supabase import create_client

SUPABASE_URL = "https://nhcevgvrdjzcazlmzrft.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oY2V2Z3ZyZGp6Y2F6bG16cmZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5NzA0OTYsImV4cCI6MjA3MzU0NjQ5Nn0.mwCUjtW16I7PKKPbSLpZK7JhgqIJDvr7KWiCkTQhAMk"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def disable_rls():
    sql1 = "ALTER TABLE user_saved_internships DISABLE ROW LEVEL SECURITY;"
    sql2 = "ALTER TABLE user_applied_internships DISABLE ROW LEVEL SECURITY;"
    try:
        supabase.rpc("sql", {"q": sql1}).execute()
        print("Disabled RLS for user_saved_internships.")
        supabase.rpc("sql", {"q": sql2}).execute()
        print("Disabled RLS for user_applied_internships.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    disable_rls()
