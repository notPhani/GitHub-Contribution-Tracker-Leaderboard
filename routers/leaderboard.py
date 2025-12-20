from flask import Blueprint, jsonify

leaderboard_bp = Blueprint("leaderboard", __name__)


LEADERBOARD_DATA = [
    {
        "rank": 1,
        "username": "a",
        "avatar": "https://avatars.githubusercontent.com/u/1024025",
        "score": 980,
        "stars": 150000,
        "repos": 6
    },
    {
        "rank": 2,
        "username": "b",
        "avatar": "https://avatars.githubusercontent.com/u/810438",
        "score": 820,
        "stars": 90000,
        "repos": 250
    },
    {
        "rank": 3,
        "username": "c",
        "avatar": "https://avatars.githubusercontent.com/u/1",
        "score": 600,
        "stars": 1200,
        "repos": 40
    }
]

@leaderboard_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    return jsonify(LEADERBOARD_DATA), 200

