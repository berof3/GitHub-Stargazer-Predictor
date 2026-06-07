#  GitHub Stargazer Predictor: Distributed ML & CI/CD Pipeline

##  Project Overview
This project implements a complete, end-to-end Data Engineering pipeline designed to predict the popularity of open-source projects. By analyzing a repository's activity signals—such as **forks, issues, watchers, and code size**—the system predicts its total **Stargazer count**.

Built from scratch on the **Swedish Science Cloud (OpenStack)**, this system serves as a demonstration of advanced cloud-native concepts, including:
*   **Infrastructure as Code (IaC):** Automated cluster orchestration using Python.
*   **Distributed Computing:** Parallelized model training using the Ray framework.
*   **Containerization:** Dependency isolation via Docker for reliable deployment.
*   **Automated CI/CD:** Zero-touch production updates using GitHooks.

###  Key Technical Achievements
*   **Automated Provisioning:** Full cluster orchestration using Python and the OpenStack API.
*   **Robust Data Harvesting:** Scaled extraction of 1,000 repositories via the GitHub REST API with autonomous rate-limit handling and pagination logic.
*   **Distributed Training:** Leveraged a 3-node **Ray Cluster** (6.0 CPUs) for exhaustive hyperparameter optimization.
*   **Portable Deployment:** Serving the final Random Forest model ($R^2 = 0.4932$) via a **Dockerized Flask API**.
*   **CI/CD Pipeline:** Implemented automated zero-touch deployment using **GitHooks**.

---

##  1. System Architecture: "The Lab-to-Shop" Paradigm
The system is logically divided into two environments to mimic professional production standards.

### Infrastructure (IaC)
Managed via a central **Manager VM**, the following nodes were provisioned:
*   **The Lab (Dev VM):** Acts as the Ray Head Node and the primary data collection hub.
*   **The Muscle (Worker 1 & 2):** Dedicated nodes providing distributed compute power for training.
*   **The Shop (Prod VM):** A standalone environment hosting the live prediction service.

> **Engineering Note:** During deployment, we successfully navigated a **Subnet IP Exhaustion** crisis by coordinating with infrastructure admins to clear "ghost" instances, ensuring all 5 nodes obtained stable internal IP assignments.

---

##  2. Methodology

### Data Collection (`scraper.py`)
Building a dataset from the GitHub API required handling high-latency and strict rate limits.
*   **Strategy:** Utilized `PyGithub` with a custom pagination loop.
*   **Robustness:** Implemented a reset-time-aware sleep logic that reads GitHub's `X-RateLimit-Reset` headers to resume harvesting automatically after throttling.
*   **Volume:** Exactly 1,000 unique repositories with $>50$ stars.

### Distributed Machine Learning (`train_model.py`)
We compared a Linear Regression baseline against an optimized **Random Forest Regressor**. To find the best "brain," we used **Ray Tune** to evaluate 12 unique hyperparameter combinations simultaneously across the cluster.

---

##  3. Scalability Analysis & Results
A core component of this project was profiling how the system scales as Virtual Machines are added to the cluster.

| Cluster Size | CPUs | Tuning Time | Speedup |
| :--- | :--- | :--- | :--- |
| 1 Node | 2.0 | 19.93s | 1.00x |
| **2 Nodes** | **4.0** | **7.97s** | **2.50x** |
| 3 Nodes | 6.0 | 7.18s | 2.77x |

### Technical Insights:
1.  **Super-Linear Speedup (2 Nodes):** We observed a 2.5x speedup with only 2.0x more CPUs. This indicates that distributing the workload reduced RAM contention and significantly improved L2/L3 cache efficiency on the Head node.
2.  **The Bottleneck (3 Nodes):** Performance gains diminished at 3 nodes. This confirms the **Communication Bottleneck** (Amdahl's Law); for a 1,000-row dataset, the network overhead of serializing data to a third machine neutralized the gain in raw processing power.

---

##  4. Production Deployment (CI/CD)
The transition from the "Lab" to the "Shop" is fully automated to ensure consistency and speed.

*   **Containerization:** The application is packaged in a **Docker** container (`Dockerfile`), isolating dependencies like Flask and Scikit-learn from the host OS.
*   **GitHooks:** A `post-receive` hook on the Production server triggers an automatic `docker build` and container restart the moment a new model is pushed from the Development VM.
*   **Live Inference (`rank_repos.py`):** Users can query the Production API at port `5100`. The model successfully ranks repositories by predicted popularity, identifying non-linear patterns that the baseline model missed.

---

##  5. Repository Structure
```text
.
├── scraper.py              # Robust GitHub data harvester
├── train_model.py          # Distributed Ray Tune training script
├── star_predictor_app.py   # Flask API for model serving
├── rank_repos.py           # Client script to test production ranking
├── Dockerfile              # Container configuration
├── github_data.csv         # The harvested 1,000-repo dataset
├── best_model.pkl          # The optimized Random Forest weights
├── scalability_report.png  # Visual proof of cluster efficiency
└── screenshots/            # Terminal logs and deployment evidence
