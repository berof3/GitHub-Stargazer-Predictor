import github
from github import Github, Auth
import pandas as pd
import time
import os

# --- 1. CONFIGURATION ---
TOKEN = "Removed my personal token for safety; Replece this line with your own token to proceed"
auth = Auth.Token(TOKEN)
g = Github(auth=auth)

print("--- Step 1: Initializing Robust Scraper ---")
repos_data = []
target_count = 1000

# Search for repos with > 50 stars, sorted by stars
query = "stars:>50"
search_results = g.search_repositories(query, sort="stars", order="desc")

print(f"Goal: Collect exactly {target_count} repositories.")

# --- 2. THE GUARANTEED LOOP ---
# We use a page-based iterator to ensure we don't miss any data
page = 0
while len(repos_data) < target_count:
    try:
        # Get a 'page' of results (GitHub gives 30 per page by default)
        current_page = search_results.get_page(page)
        
        if not current_page:
            print("No more repositories found.")
            break
            
        for repo in current_page:
            if len(repos_data) >= target_count:
                break
                
            repos_data.append({
                "full_name": repo.full_name,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "watchers": repo.subscribers_count,
                "size": repo.size,
                "has_wiki": int(repo.has_wiki),
                "has_pages": int(repo.has_pages),
                "stars": repo.stargazers_count
            })

        print(f"Progress: {len(repos_data)}/{target_count} collected...")
        page += 1
        
        # Respect Search API rate limits (30 requests per minute)
        # We pause slightly between pages
        time.sleep(2)

    except github.RateLimitExceededException:
        print("\n!!! GitHub Rate Limit Hit !!!")
        search_limit = g.get_rate_limit().search
        reset_timestamp = search_limit.reset.timestamp()
        sleep_time = max(reset_timestamp - time.time(), 0) + 5
        print(f"Sleeping for {int(sleep_time)} seconds until limit resets...")
        time.sleep(sleep_time)
        continue # Try the same page again after sleep

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(10)
        continue

# --- 3. SAVE DATA ---
df = pd.DataFrame(repos_data)
df.to_csv("github_data.csv", index=False)

print(f"\nSUCCESS: Exactly {len(df)} unique repositories saved to github_data.csv")
