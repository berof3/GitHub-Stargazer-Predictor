from flask import Flask, request, jsonify, render_template_string
import pickle
import pandas as pd
import time

app = Flask(__name__)

# 1. Load the model once at startup (not inside the route!)
with open('best_model.pkl', 'rb') as f:
    model = pickle.load(f)

# 2. Pre-defined Test Repositories
test_repos_raw = [
    {"name": "Repo_A (Small Utility)", "forks": 10, "open_issues": 2, "watchers": 5, "size": 500, "has_wiki": 0, "has_pages": 0},
    {"name": "Repo_B (Growing Tool)", "forks": 150, "open_issues": 25, "watchers": 80, "size": 3000, "has_wiki": 1, "has_pages": 0},
    {"name": "Repo_C (Popular Framework)", "forks": 2500, "open_issues": 120, "watchers": 1500, "size": 15000, "has_wiki": 1, "has_pages": 1},
    {"name": "Repo_D (Stable Library)", "forks": 600, "open_issues": 15, "watchers": 400, "size": 8000, "has_wiki": 1, "has_pages": 1},
    {"name": "Repo_E (Legacy Script)", "forks": 5, "open_issues": 40, "watchers": 2, "size": 100, "has_wiki": 0, "has_pages": 0}
]

@app.route('/')
def home():
    return "<h1>GitHub Stargazer Predictor</h1><p>Visit <b>/results</b> to see the ranking.</p>"

@app.route('/results')
def show_results():
    input_df = pd.DataFrame([ {k:v for k,v in r.items() if k != 'name'} for r in test_repos_raw ])
    
    # AI calculates all 5 predictions in one single operation!
    predictions = model.predict(input_df)
    
    # Combine names with results
    results = []
    for i in range(len(test_repos_raw)):
        results.append({
            "name": test_repos_raw[i]["name"], 
            "predicted_stars": int(predictions[i])
        })
    
    # Sort by stars
    ranked = sorted(results, key=lambda x: x['predicted_stars'], reverse=True)

    # HTML Table Output
    html = "<h2>Final Ranking of Repositories</h2><table border='1'><tr><th>Rank</th><th>Repository Name</th><th>Predicted Stars</th></tr>"
    for i, r in enumerate(ranked, 1):
        html += f"<tr><td>{i}</td><td>{r['name']}</td><td>{r['predicted_stars']}</td></tr>"
    html += "</table>"
    return html

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]
    return jsonify({"predicted_stars": int(prediction), "status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
