from supabase import create_client

SUPABASE_URL = "https://nhcevgvrdjzcazlmzrft.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oY2V2Z3ZyZGp6Y2F6bG16cmZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5NzA0OTYsImV4cCI6MjA3MzU0NjQ5Nn0.mwCUjtW16I7PKKPbSLpZK7JhgqIJDvr7KWiCkTQhAMk"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def disable_rls():
    sql = "ALTER TABLE internships DISABLE ROW LEVEL SECURITY;"
    response = supabase.rpc("sql", {"q": sql}).execute()
    if response.get("error"):
        print("Error disabling RLS:", response.get("error"))
    else:
        print("RLS disabled for internships.")

if __name__ == "__main__":
    disable_rls()
