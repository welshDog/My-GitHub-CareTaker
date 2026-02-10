import os
from flask import Flask, render_template, jsonify, request

from caretaker.core.config import get_token, get_username, get_base_url
from caretaker.core.github_client import GitHubClient
from caretaker.plugins import load_plugins, CareContext
from caretaker.core.reporting import write_json
from caretaker.plugins.duplicates import DuplicatesPlugin

app = Flask(__name__, template_folder="templates", static_folder="static")

client = GitHubClient(get_token(), get_base_url())
ctx = CareContext(client, get_username())
plugins = load_plugins()

@app.route("/")
def index():
    repos = client.list_user_repos(ctx.owner)
    return render_template("index.html", repos=repos)

@app.route("/run/<name>")
def run_plugin(name):
    for p in plugins:
        if p.name == name:
            result = p.run(ctx)
            write_json(os.path.join(os.getcwd(), "reports"), f"{name}", result)
            return jsonify(result)
    return jsonify({"error": "plugin not found"}), 404

@app.route("/repos")
def repos():
    repos = client.list_user_repos(ctx.owner)
    return render_template("repos.html", repos=repos)

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/cleanup/duplicates", methods=["POST"])
def cleanup_duplicates():
    p = DuplicatesPlugin()
    result = p.run(ctx)
    archived = []
    groups = result.get("groups", {})
    for _, items in groups.items():
        if len(items) <= 1:
            continue
        hero = sorted(items, key=lambda x: x.get("pushed_at") or x.get("updated_at"), reverse=True)[0]
        for r in items:
            if r["name"] == hero["name"]:
                continue
            ok = client.archive_repo(ctx.owner, r["name"])
            archived.append({"repo": r["name"], "archived": ok})
    write_json(os.path.join(os.getcwd(), "reports"), "cleanup_duplicates", {"archived": archived})
    return jsonify({"archived": archived})

def create_app():
    return app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
