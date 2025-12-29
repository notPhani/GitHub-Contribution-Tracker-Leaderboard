from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)
print("DEBUG GITHUB_CLIENT_ID:", os.getenv("GITHUB_CLIENT_ID"))

from flask import Flask, render_template, redirect, request, session
import requests
from routers.profile import profile_bp, get_github_user_data
from routers.leaderboard import leaderboard_bp

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

# Register blueprint
app.register_blueprint(profile_bp, url_prefix="/api")
app.register_blueprint(leaderboard_bp, url_prefix="/api")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}&scope=read:user"
    )
    return redirect(github_auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "Authorization failed", 400

    # Exchange code for access token
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return "Failed to retrieve access token", 400

    session["access_token"] = access_token

    # Fetch and store user data in Supabase
    try:
        user_data = get_github_user_data(access_token)
        if user_data:
            session["user_id"] = user_data.get("username")
    except Exception as e:
        print(f"Error storing user data: {e}")
        # Continue anyway - user can still access the app

    return redirect("/leaderboard")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


if __name__ == "__main__":
    app.run(debug=True)