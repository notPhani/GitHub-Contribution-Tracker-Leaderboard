from supabase import create_client, Client
import os
from typing import Dict, List, Optional

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_user_by_github_id(github_id: int) -> Optional[Dict]:
    """Get user by GitHub ID"""
    try:
        response = supabase.table('users').select('*').eq('github_id', github_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user by GitHub ID: {e}")
        return None

def create_or_update_user(user_data: Dict) -> Optional[Dict]:
    """Create or update user in database"""
    try:
        # Check if user exists
        existing_user = get_user_by_github_id(user_data['github_id'])

        if existing_user:
            # Update existing user
            response = supabase.table('users').update(user_data).eq('github_id', user_data['github_id']).execute()
            return response.data[0] if response.data else None
        else:
            # Create new user
            response = supabase.table('users').insert(user_data).execute()
            return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating/updating user: {e}")
        return None

def get_leaderboard_users(limit: int = 50) -> List[Dict]:
    """Get top users for leaderboard"""
    try:
        response = supabase.table('users').select('*').order('score', desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"Error getting leaderboard: {e}")
        return []

def calculate_user_score(user_data: Dict) -> int:
    """Calculate user score based on GitHub metrics"""
    # Heuristic scoring algorithm: (stars, repos, followers, commits, gists)
    stars_weight = 5
    repos_weight = 2
    followers_weight = 3
    commits_weight = 1
    gists_weight = 0.5

    score = (
        user_data.get('total_stars', 0) * stars_weight +
        user_data.get('public_repos', 0) * repos_weight +
        user_data.get('followers', 0) * followers_weight +
        user_data.get('total_commits', 0) * commits_weight +
        user_data.get('public_gists', 0) * gists_weight
    )

    return int(score)

def update_user_score(github_id: int) -> bool:
    """Recalculate and update user score"""
    try:
        user = get_user_by_github_id(github_id)
        if not user:
            return False

        new_score = calculate_user_score(user)
        supabase.table('users').update({'score': new_score}).eq('github_id', github_id).execute()
        return True
    except Exception as e:
        print(f"Error updating user score: {e}")
        return False