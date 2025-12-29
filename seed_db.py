#!/usr/bin/env python3
"""
Database setup and seeding script for GitHub Contribution Tracker
Run this after setting up Supabase and updating your .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from db import supabase, create_or_update_user, calculate_user_score

def seed_sample_users():
    """Add some sample users to the database for testing"""

    sample_users = [
        {
            "github_id": 1,
            "username": "octocat",
            "name": "The Octocat",
            "email": "octocat@github.com",
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "bio": "GitHub's mascot",
            "location": "San Francisco",
            "company": "GitHub",
            "public_repos": 12,
            "public_gists": 5,
            "followers": 240,
            "following": 12,
            "total_stars": 150,
            "total_commits": 450,
        },
        {
            "github_id": 2,
            "username": "torvalds",
            "name": "Linus Torvalds",
            "email": "torvalds@linux-foundation.org",
            "avatar_url": "https://avatars.githubusercontent.com/u/1024025?v=4",
            "bio": "Linux kernel creator",
            "location": "Portland, OR",
            "company": "Linux Foundation",
            "public_repos": 6,
            "public_gists": 0,
            "followers": 180000,
            "following": 0,
            "total_stars": 2000,
            "total_commits": 30000,
        },
        {
            "github_id": 4,
            "username": "notPhani",
            "name": "Not Phani",
            "email": "notphani@example.com",
            "avatar_url": "https://avatars.githubusercontent.com/u/12345678?v=4",
            "bio": "Just another developer",
            "location": "Somewhere",
            "company": "Some Company",
            "public_repos": 15,
            "public_gists": 3,
            "followers": 50,
            "following": 25,
            "total_stars": 200,
            "total_commits": 800,
        }
    ]

    print("Seeding sample users...")

    for user_data in sample_users:
        # Calculate score
        user_data["score"] = calculate_user_score(user_data)

        # Create or update user
        result = create_or_update_user(user_data)
        if result:
            print(f"✓ Added/Updated user: {user_data['username']}")
        else:
            print(f"✗ Failed to add user: {user_data['username']}")

    print("Seeding complete!")

if __name__ == "__main__":
    # Check if Supabase is configured
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("❌ Please set SUPABASE_URL and SUPABASE_KEY in your .env file")
        exit(1)

    try:
        # Test connection
        supabase.table('users').select('count').limit(1).execute()
        print("✅ Supabase connection successful")
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("Make sure your database schema is set up (run schema.sql in Supabase SQL Editor)")
        exit(1)

    seed_sample_users()