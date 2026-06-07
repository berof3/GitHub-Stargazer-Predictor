import requests
import json

# The Production API URL
URL = "http://130.238.27.21:5100/predict"

# 5 Repositories to Test (Features: forks, issues, watchers, size, wiki, pages)
test_repos = [
    {"name": "Repo_A (Small Utility)", "data": {"forks": 10, "open_issues": 2, "watchers": 5, "size": 500, "has_wiki": 0, "has_pages": 0}},
    {"name": "Repo_B (Growing Tool)", "data": {"forks": 150, "open_issues": 25, "watchers": 80, "size": 3000, "has_wiki": 1, "has_pages": 0}},
    {"name": "Repo_C (Popular Framework)", "data": {"forks": 2500, "open_issues": 120, "watchers": 1500, "size": 15000, "has_wiki": 1, "has_pages": 1}},
    {"name": "Repo_D (Stable Library)", "data": {"forks": 600, "open_issues": 15, "watchers": 400, "size": 8000, "has_wiki": 1, "has_pages": 1}},
    {"name": "Repo_E (Legacy Script)", "data": {"forks": 5, "open_issues": 40, "watchers": 2, "size": 100, "has_wiki": 0, "has_pages": 0}}
]

results = []

print("--- Querying Production AI Model ---")
for repo in test_repos:
    response = requests.post(URL, json=repo["data"])
    prediction = response.json()["predicted_stars"]
    results.append({"name": repo["name"], "predicted_stars": prediction})
    print(f"Predicted Stars for {repo['name']}: {prediction}")

# Sort the repositories by stars (Descending)
ranked_results = sorted(results, key=lambda x: x['predicted_stars'], reverse=True)

print("\n" + "="*40)
print("FINAL RANKING")
print("="*40)
for i, repo in enumerate(ranked_results, 1):
    print(f"{i}. {repo['name']} - Predicted Stars: {repo['predicted_stars']}")
print("="*40)
