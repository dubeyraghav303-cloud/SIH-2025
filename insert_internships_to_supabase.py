import pandas as pd
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://nhcevgvrdjzcazlmzrft.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oY2V2Z3ZyZGp6Y2F6bG16cmZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5NzA0OTYsImV4cCI6MjA3MzU0NjQ5Nn0.mwCUjtW16I7PKKPbSLpZK7JhgqIJDvr7KWiCkTQhAMk"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load CSV
df = pd.read_csv("pmis_internships.csv")

# Process data
df.rename(columns={'InternshipID': 'id', 'RoleTitle': 'title', 'Skills': 'required_skills', 'Sector': 'sector_interests', 'City': 'location', 'Stipend_INR': 'stipend', 'Company': 'company'}, inplace=True)
df['id'] = df['id'].str.split('-').str[1].astype(int)
df['description'] = df['company'] + ' - ' + df['title']
df['required_skills'] = df['required_skills'].str.split(',').apply(lambda x: [s.strip() for s in x])
df['sector_interests'] = df['sector_interests'].str.split(',').apply(lambda x: [s.strip() for s in x])

# Convert to dict
internships = df[['id', 'title', 'description', 'required_skills', 'sector_interests', 'location', 'stipend', 'company']].to_dict(orient='records')

# IMPORTANT: Temporarily disable RLS manually in Supabase dashboard for internships table before running this script

# Insert into Supabase
response = supabase.table('internships').upsert(internships).execute()
print("Inserted internships:", response)

# After running, re-enable RLS manually in Supabase dashboard for internships table
