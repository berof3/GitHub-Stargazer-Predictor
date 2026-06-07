
# 🚀 GitHub Stargazer Predictor: Distributed ML & CI/CD Pipeline

This project implements an end-to-end Data Engineering pipeline to predict GitHub repository popularity. It covers the full lifecycle: from automated infrastructure provisioning to distributed training and containerized production serving.

## 📁 Repository Structure
```text
.
├── cicd/                   # CI/CD Automation
│   └── post-receive        # GitHook for automated production rebuilds
├── data/                   # Dataset Storage
│   └── github_data.csv     # Harvested 1,000-repo dataset
├── data_pipeline/          # Data Acquisition Logic
│   └── scraper.py          # Robust GitHub REST API harvester
├── docs/                   # Documentation & Evidence
│   └── screenshots/        # Terminal logs and deployment proof
├── infrastructure/         # Infrastructure as Code (IaC)
│   ├── launch_VMs.py       # OpenStack Python orchestrator
│   └── cloud-cfg.txt       # Cloud-init contextualization script
├── production/             # Deployment & Inference
│   ├── star_predictor_app.py # Flask API serving the model
│   ├── Dockerfile          # Container configuration
│   └── rank_repos.py       # Client-side inference/test script
└── training/               # Distributed Machine Learning
    ├── train_model.py      # Ray Tune training script
    ├── best_model.pkl      # Serialized Random Forest weights
    ├── plot_scalability.py # Analysis visualization script
    └── tuning_results_*.csv # Scalability performance metrics

### System Architecture
The system follows a Lab-to-Shop paradigm:
The Lab (Development): Data is harvested and the model is tuned across a 3-node Ray Cluster.
The Bridge (CI/CD): GitHooks automate the movement of model artifacts from the Lab to the Shop.
The Shop (Production): The model is served as a Machine Learning as a Service (MLaaS) via Docker.
#### roducibility Guide
Provisioning: Run infrastructure/launch_VMs.py on your Manager node.
Harvesting: Execute data_pipeline/scraper.py to build the training set.
Training: Run training/train_model.py to perform distributed hyperparameter search.
Deployment: Commit changes and run git push production main to trigger the automated rebuild.
Testing: Run production/rank_repos.py to query the live API.
