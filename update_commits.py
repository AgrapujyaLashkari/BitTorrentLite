import time, random, subprocess, datetime

# --- your identity ---
NAME = b"Agrapujya Lashkari"
EMAIL = b"joebrion20@gmail.com"

# --- configuration ---
DAYS_SPAN = 5  # spread over 5 days
END_DATE = datetime.datetime(2025, 10, 31, 22, 35, 0)  # last commit time (UTC)

# --- get commits (oldest first) ---
commits = subprocess.check_output(
    ["git", "rev-list", "--reverse", "HEAD"]
).decode().splitlines()

num_commits = len(commits)

# Convert end date to timestamp
end_ts = int(END_DATE.timestamp())
start_ts = end_ts - DAYS_SPAN * 24 * 3600

# Calculate average gap
avg_gap = (end_ts - start_ts) // max(1, num_commits - 1)
cur = start_ts

# Write mapping file for timestamps
mapping_file = ".git/map.txt"
with open(mapping_file, "w") as f:
    for c in commits:
        f.write(f"{c}::{cur}\n")
        gap = int(avg_gap * random.uniform(0.6, 1.4))
        cur += gap
        if cur > end_ts:
            cur = end_ts

# --- rewrite commits with git-filter-repo ---
subprocess.run([
    "git", "filter-repo", "--force",
    "--commit-callback",
    (
        f"mapping = dict(line.strip().split('::') for line in open('{mapping_file}'))\n"
        f"ts = mapping[commit.original_id.decode()]\n"
        f"commit.author_name = {NAME!r}\n"
        f"commit.author_email = {EMAIL!r}\n"
        f"commit.committer_name = {NAME!r}\n"
        f"commit.committer_email = {EMAIL!r}\n"
        f"commit.author_date = commit.committer_date = ts.encode() + b' +0000'\n"
    )
])
