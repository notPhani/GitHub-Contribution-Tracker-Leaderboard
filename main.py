from flask import Flask, render_template, redirect, request, session
import requests

from routers.profile import profile_bp

app = Flask(__name__)
app.secret_key = "dev-secret-key"

GITHUB_CLIENT_ID = "Ov23liBF0Qu16ZiUL6FM"
GITHUB_CLIENT_SECRET = "80981731563ac0a804d16721bc5be662c90f5e69"

app.register_blueprint(profile_bp, url_prefix="/api")


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

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )

    session["access_token"] = token_response.json().get("access_token")

    return redirect("/profile")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")

print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
