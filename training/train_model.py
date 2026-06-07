import pandas as pd
import numpy as np
import ray
from ray import tune
import time
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# 1. Initialize Ray and Print Cluster Status
ray.init(ignore_reinit_error=True)

nodes = ray.nodes()
active_workers = len([node for node in nodes if node["Alive"]])
total_cpus = ray.cluster_resources().get("CPU", 0)

print("\n" + "="*40)
print("RAY CLUSTER TELEMETRY")
print("="*40)
print(f"Status:          CONNECTED")
print(f"Active Nodes:    {active_workers}")
print(f"Total CPU Cores: {total_cpus}")
print("="*40 + "\n")

# 2. Load Data
df = pd.read_csv('github_data.csv')
features = ['forks', 'open_issues', 'watchers', 'size', 'has_wiki', 'has_pages']
X = df[features].values
y = df['stars'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- MODEL 1: Baseline ---
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_r2 = r2_score(y_test, lr.predict(X_test))

# --- MODEL 2: Native Ray Tune Distributed Search ---
def train_rf(config):
    model = RandomForestRegressor(
        n_estimators=config["n_estimators"],
        max_depth=config["max_depth"],
        random_state=42
    )
    model.fit(X_train, y_train)
    score = r2_score(y_test, model.predict(X_test))
    return {"r2": score}

search_space = {
    "n_estimators": tune.grid_search([50, 100, 200]),
    "max_depth": tune.grid_search([5, 10, None])
}

print(f"Starting Grid Search on {active_workers} nodes...")
start_time = time.time()

tuner = tune.Tuner(train_rf, param_space=search_space)
results = tuner.fit()

end_time = time.time()
total_duration = end_time - start_time

# 3. Export Results to Table
# This creates the data needed for our Scalability Graphs
results_df = results.get_dataframe()
# We add the node count so we can merge files later
results_df["node_count"] = active_workers
results_df["total_tuning_time"] = total_duration

output_filename = f"tuning_results_{active_workers}_nodes.csv"
results_df.to_csv(output_filename, index=False)

# 4. Final Summary
best_result = results.get_best_result(metric="r2", mode="max")
print("\n" + "="*40)
print("SCIENTIFIC REPORT SUMMARY")
print("="*40)
print(f"Baseline R2:        {lr_r2:.4f}")
print(f"Best Tuned RF R2:   {best_result.metrics['r2']:.4f}")
print(f"Best Config:        {best_result.config}")
print(f"Total Tuning Time:  {total_duration:.2f}s")
print(f"Results saved to:   {output_filename}")
print("="*40)

# Save best model
best_model = RandomForestRegressor(**best_result.config)
best_model.fit(X_train, y_train)
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

ray.shutdown()
