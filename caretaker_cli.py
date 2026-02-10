import os
import json
from caretaker.core.config import get_token, get_username, get_base_url
from caretaker.core.github_client import GitHubClient
from caretaker.plugins import load_plugins, CareContext
from caretaker.core.reporting import write_json

def main():
    client = GitHubClient(get_token(), get_base_url())
    ctx = CareContext(client, get_username())
    out = {}
    for p in load_plugins():
        out[p.name] = p.run(ctx)
    path = write_json(os.path.join(os.getcwd(), "reports"), "summary", out)
    print(path)

if __name__ == "__main__":
    main()

