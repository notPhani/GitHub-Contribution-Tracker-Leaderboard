from flask import Flask
from flask_cors import CORS

from routers.leaderboard import leaderboard_bp

app = Flask(__name__)
CORS(app)


app.register_blueprint(leaderboard_bp)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
