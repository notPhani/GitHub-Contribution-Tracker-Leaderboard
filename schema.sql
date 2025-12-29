-- Create users table for storing GitHub user data
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    avatar_url TEXT,
    bio TEXT,
    location VARCHAR(255),
    company VARCHAR(255),
    blog TEXT,
    twitter_username VARCHAR(255),
    public_repos INTEGER DEFAULT 0,
    public_gists INTEGER DEFAULT 0,
    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    total_stars INTEGER DEFAULT 0,
    total_commits INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on github_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_github_id ON users(github_id);

-- Create index on score for leaderboard queries
CREATE INDEX IF NOT EXISTS idx_users_score ON users(score DESC);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();