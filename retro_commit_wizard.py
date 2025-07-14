# RetroCommitWizard: create retroactive git commits with custom dates for crypto farming

import os
import random
import subprocess
import time
from datetime import datetime, timedelta

# === Configuration ===
MAX_DAYS_BACK = 850
REPO_PATHS = ["./"]  # assuming script runs inside repo root
USERNAME = "imasterrr"
EMAIL = "your-email@example.com"

def generate_commit_message():
    verbs = ["Fix", "Add", "Improve", "Update", "Refactor", "Remove", "Optimize"]
    objects = ["wallet", "transaction", "balance", "token", "signature", "network", "script"]
    contexts = ["logic", "code", "function", "flow", "module", "handler"]
    return f"{random.choice(verbs)} {random.choice(objects)} {random.choice(contexts)}"

def modify_file():
    target = "retro_commit_wizard.py"
    with open(target, "a") as f:
        line = f"# Update note {random.randint(1000, 9999)}\n"
        f.write(line)

def main():
    used_days = set()
    if os.path.exists("farm_state.txt"):
        with open("farm_state.txt", "r") as f:
            used_days = set(map(int, f.read().strip().split(",")))

    available_days = [d for d in range(MAX_DAYS_BACK) if d not in used_days]
    if not available_days:
        print("✅ All days used.")
        return

    commits_today = random.randint(1, 5)
    print(f"🗓 Commits today: {commits_today}")

    for i in range(commits_today):
        if not available_days:
            break
        chosen_day = random.choice(available_days)
        available_days.remove(chosen_day)
        used_days.add(chosen_day)

        commit_date = datetime.now() - timedelta(days=chosen_day)
        date_str = commit_date.replace(
            hour=random.randint(7, 11),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        ).strftime("%Y-%m-%dT%H:%M:%S")

        modify_file()

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "config", "user.name", USERNAME], check=True)
        subprocess.run(["git", "config", "user.email", EMAIL], check=True)

        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        commit_message = generate_commit_message()
        subprocess.run(["git", "commit", "-m", commit_message], env=env, check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        with open("farm_log.txt", "a") as flog:
            flog.write(f"{datetime.now().isoformat()} | COMMIT #{i+1} | Date: {date_str} | Message: {commit_message}\n")

        time.sleep(random.randint(15, 30))

    with open("farm_state.txt", "w") as f:
        f.write(",".join(map(str, sorted(used_days))))

if __name__ == "__main__":
    main()
