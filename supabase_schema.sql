-- Enable UUID extension if not already
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create profiles table
CREATE TABLE profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT,
    email TEXT,
    education TEXT,
    skills TEXT[],
    sectors TEXT[],
    experience INTEGER,
    institution TEXT,
    preferred_locations TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create internships table
CREATE TABLE internships (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    required_skills TEXT[],
    sector_interests TEXT[],
    location TEXT,
    stipend INTEGER,
    company TEXT
);

-- Create user_saved_internships table
CREATE TABLE user_saved_internships (
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    internship_id INTEGER REFERENCES internships(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, internship_id)
);

-- Create user_applied_internships table
CREATE TABLE user_applied_internships (
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    internship_id INTEGER REFERENCES internships(id) ON DELETE CASCADE,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, internship_id)
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_saved_internships ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_applied_internships ENABLE ROW LEVEL SECURITY;

-- Policies for profiles
CREATE POLICY "Users can view their own profile" ON profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own profile" ON profiles
    FOR UPDATE USING (auth.uid() = user_id);

-- Policies for user_saved_internships
CREATE POLICY "Users can view their own saved internships" ON user_saved_internships
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own saved internships" ON user_saved_internships
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own saved internships" ON user_saved_internships
    FOR DELETE USING (auth.uid() = user_id);

-- Policies for user_applied_internships
CREATE POLICY "Users can view their own applied internships" ON user_applied_internships
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own applied internships" ON user_applied_internships
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Allow anyone to view internships (public)
ALTER TABLE internships ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view internships" ON internships FOR SELECT USING (true);
