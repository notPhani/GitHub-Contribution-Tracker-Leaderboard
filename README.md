# GitHub Contribution Tracker Leaderboard

A Flask web application that tracks GitHub user contributions and displays a leaderboard using Supabase as the database.

## Features

- GitHub OAuth authentication
- User profile data collection from GitHub API
- Dynamic leaderboard with scoring algorithm
- Supabase database integration
- Responsive web interface

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Rashi-08/GitHub-Contribution-Tracker-Leaderboard.git
cd GitHub-Contribution-Tracker-Leaderboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to your project settings and copy:
   - Project URL
   - Project API Key (anon/public key)

### 4. Set up GitHub OAuth

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set Authorization callback URL to: `http://localhost:5000/callback`
4. Copy Client ID and Client Secret

### 5. Configure environment variables

Create a `.env` file in the root directory:

```env
# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
FLASK_SECRET_KEY=your_random_secret_key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

### 6. Set up database schema

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Run the SQL from `schema.sql` to create the users table

### 7. Seed sample data (optional)

Run the seeding script to add sample users for testing:

```bash
python seed_db.py
```

### 8. Run the application
```bash
python main.py
```

Visit `http://localhost:5000` to access the application.

## Scoring Algorithm

The leaderboard uses a heuristic scoring system:

```
Score = (total_stars × 2) + (public_repos × 10) + (followers × 5) + (total_commits × 1) + (public_gists × 0.5)
```

## API Endpoints

- `GET /api/profile` - Get current user profile (requires authentication)
- `GET /api/leaderboard` - Get leaderboard data

## Database Schema

The `users` table stores comprehensive GitHub user data including:
- Basic profile information (username, name, email, avatar)
- GitHub metrics (repos, stars, followers, commits)
- Calculated score for leaderboard ranking
- Timestamps for creation and updates

## Architecture

- **Frontend**: HTML templates with JavaScript for dynamic content
- **Backend**: Flask with blueprint architecture
- **Database**: Supabase (PostgreSQL)
- **Authentication**: GitHub OAuth 2.0
- **API**: RESTful endpoints for data exchange