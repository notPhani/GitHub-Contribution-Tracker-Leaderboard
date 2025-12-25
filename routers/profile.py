from flask import Blueprint, jsonify, session
import requests

profile_bp = Blueprint("profile", __name__)

GITHUB_API = "https://api.github.com"


def calculate_score(stars, repos, followers):
    return stars * 2 + repos * 10 + followers * 5


def get_github_user(access_token):
    headers = {
        "Authorization": f"token {access_token}"
    }

    user_res = requests.get(f"{GITHUB_API}/user", headers=headers)
    repos_res = requests.get(f"{GITHUB_API}/user/repos", headers=headers)

    user_data = user_res.json()
    repos_data = repos_res.json()

    total_stars = sum(repo["stargazers_count"] for repo in repos_data)

    return {
        "username": user_data.get("login"),
        "avatar": user_data.get("avatar_url"),
        "bio": user_data.get("bio"),
        "followers": user_data.get("followers"),
        "public_repos": user_data.get("public_repos"),
        "stars": total_stars
    }


@profile_bp.route("/profile", methods=["GET"])
def profile():
    if "access_token" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_github_user(session["access_token"])

    score = calculate_score(
        stars=user["stars"],
        repos=user["public_repos"],
        followers=user["followers"]
    )

    return jsonify({
        "username": user["username"],
        "avatar": user["avatar"],
        "bio": user["bio"],
        "followers": user["followers"],
        "public_repos": user["public_repos"],
        "stars": user["stars"],
        "score": score,
        "tags": ["AI", "Web"]
    }), 200