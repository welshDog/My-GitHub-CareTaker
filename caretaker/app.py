import os
from flask import Flask, render_template, jsonify, request

from caretaker.core.config import get_username
from caretaker.plugins import load_plugins, get_plugin
from caretaker.core.context import build_context
from caretaker.core.reporting import write_json

app = Flask(__name__, template_folder="templates", static_folder="static")

# Global initialization using shared context factory
# We don't pass an owner yet, will rely on config
# Ideally, owner should be per-request or from config
ctx = build_context()

# Ensure MonitorAgent is attached to context
if not ctx.monitor:
    monitor_agent = get_plugin('monitor')
    ctx.monitor = monitor_agent
    # Note: monitor_agent is not started here, just attached.
    # If run_plugin('monitor') is called, it will run.

# Pre-load plugins for the API availability
plugins = load_plugins()

@app.route("/")
def index():
    repos = ctx.client.list_user_repos(ctx.owner)
    return render_template("index.html", repos=repos)

@app.route("/run/<name>")
def run_plugin(name):
    # Dynamic plugin loading ensures we get the latest or correct one
    # But for simplicity we can iterate the loaded list or use get_plugin
    p = get_plugin(name)
    if p:
        result = p.run(ctx)
        write_json(os.path.join(os.getcwd(), "reports"), f"{name}", result)
        return jsonify(result)
    return jsonify({"error": "plugin not found"}), 404

@app.route("/repos")
def repos():
    repos = ctx.client.list_user_repos(ctx.owner)
    return render_template("repos.html", repos=repos)

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/cleanup/duplicates", methods=["POST"])
def cleanup_duplicates():
    p = get_plugin('duplicates')
    if not p:
         return jsonify({"error": "duplicates plugin not found"}), 500
         
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
            ok = ctx.client.archive_repo(ctx.owner, r["name"])
            archived.append({"repo": r["name"], "archived": ok})
    write_json(os.path.join(os.getcwd(), "reports"), "cleanup_duplicates", {"archived": archived})
    return jsonify({"archived": archived})

def create_app():
    return app

if __name__ == "__main__":
    # Security: Bind only to localhost
    app.run(host="127.0.0.1", port=5001)
