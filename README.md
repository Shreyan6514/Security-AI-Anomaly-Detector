AI-Driven Security Anomaly Detector

🛡️ Project Overview

This project is a high-security E-Commerce API built with FastAPI and an integrated Neural Network monitor. It fulfills the requirements for the "Identification and Analysis of Threats" module (Grade 5 level), demonstrating how machine learning can identify and mitigate cybersecurity threats in real-time.

💻 Technical Implementation & M1 Optimization

For this project, Python 3.13 and Scikit-Learn were selected over JavaScript-based alternatives for several critical reasons:

Apple Silicon (M1) Performance: Python’s data science stack (Numpy, Pandas) has native ARM64 support, allowing the Neural Network to run efficiently on the M1 chip's architecture.

Feature Scaling: Using StandardScaler from Scikit-Learn was essential to normalize disparate data points (like Status Codes vs. Durations), ensuring accurate risk scoring.

Dependency Stability: Python provided a stable virtual environment (.venv), avoiding the compilation issues often found with Node.js C++ bindings on Apple Silicon.

🚀 How to Run the Project

1. Prerequisites

Ensure you have Python 3.10+ installed on your system.

2. Setup Environment

# Clone the repository
git clone [YOUR_GITHUB_URL_HERE]
cd [YOUR_PROJECT_FOLDER]

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .\.venv\Scripts\activate # Windows

# Install dependencies
pip install -r requirements.txt


3. Start the API Server

uvicorn main:app --reload


The API will be available at http://127.0.0.1:8000. You can use Postman to send requests to /token, /products, and /order.

4. Run AI Security Analysis

Open a second terminal window (keep the API running) and run:

python3 security_brain.py


This will process the traffic_logs.csv and output a real-time risk audit.

📊 Security Features

OAuth2 Authentication: Secure token-based access control.

Traffic Logging Middleware: Automated feature extraction (Status, Path Length, Duration).

Neural Network (MLPClassifier): Anomaly detection that flags "High Risk" scores for suspicious patterns.

Automated Mitigation: Simulated firewall triggers for scores > 0.4.

Author: Shreyan

Module: Identification and Analysis of Threats (Grade 5 Project)
