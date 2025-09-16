# TODO: Add Supabase Integration to Flask App

## Step 1: Set Up Supabase Project
- [x] Guide user to create Supabase project at https://supabase.com
- [x] Get Supabase URL and anon key
- [x] Create database tables in Supabase:
  - [x] Run supabase_schema.sql in Supabase SQL editor

## Step 2: Install Dependencies
- [x] Install supabase-py: pip install supabase

## Step 3: Update Flask App (app.py)
- [x] Import supabase and initialize client with URL and key
- [x] Modify login route to authenticate user with Supabase auth
- [x] Add signup route for new users
- [x] Update onboarding routes to save profile data to Supabase
- [x] Update internship_form route to save user input to profile
- [x] Update save_toggle route to save/unsave internships in Supabase
- [x] Update submit_application route to save applied internships in Supabase
- [x] Update profile route to fetch data from Supabase
- [x] Load internships from Supabase instead of CSV (optional, but recommended)

## Step 4: Update Templates if Needed
- [x] Modify login.html for email/password login
- [x] Add signup.html template
- [x] Ensure profile.html displays data from Supabase

## Step 5: Test Integration
- [x] Run the app and test user registration, login, onboarding, saving/applying internships
- [x] Verify data is saved and retrieved correctly from Supabase
- [x] Update profile.html to display full internship details (company, skills, location, stipend) for saved and applied internships
