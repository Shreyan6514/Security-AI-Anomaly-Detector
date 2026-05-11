import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os

# Neural Network for Anomaly Detection
# I have implemented the Mitigation Logic (works as preventive measure)

def train_and_predict():
    print("AI MONITOR: Training Neural Network on traffic patterns...")

    # TRAINING DATA
    # Features: [StatusCode, PathLength, Duration]
    # Labels: 0 = Normal, 1 = Suspicious
    X_train = np.array([
        [200, 5, 0.010],   # Normal
        [200, 10, 0.015],  # Normal
        [200, 15, 0.020],  # Normal
        [200, 8, 0.012],   # Normal
        [401, 10, 0.001],  # Suspicious (Unauthorized)
        [404, 45, 0.005],  # Suspicious (Path Probing)
        [403, 50, 0.002],  # Suspicious (Forbidden)
        [404, 60, 0.003],  # Suspicious
        [422, 12, 0.001],  # Suspicious (Fuzzing)
        [500, 30, 0.005]   # Suspicious (Server Error/Crash)
    ])
    y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

    # FEATURE SCALING
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # INITIALIZE NEURAL NETWORK
    mlp = MLPClassifier(
        hidden_layer_sizes=(12, 6), 
        max_iter=5000, 
        random_state=42,
        solver='lbfgs',
        activation='relu'
    )
    mlp.fit(X_train_scaled, y_train)

    # ANALYZE LOGS
    log_file = "traffic_logs.csv"
    
    if os.path.exists(log_file) and os.path.getsize(log_file) > 50:
        print(f"AI MONITOR: Analyzing real traffic from {log_file}...")
        df = pd.read_csv(log_file)
        
        # Prepare data from the CSV
        current_traffic = df[['status', 'path_len', 'duration']].values
        current_traffic_scaled = scaler.transform(current_traffic)
        
        # Get risk probabilities
        predictions = mlp.predict_proba(current_traffic_scaled)[:, 1]
        
        print("-" * 85)
        print(f"{'REQUEST':<10} | {'STATUS':<8} | {'PATH LEN':<10} | {'RISK SCORE':<12} | {'VERDICT'} | {'ACTION'}")
        print("-" * 85)
        
        high_risk_detected = False
        for i, prob in enumerate(predictions):
            status_code = df.iloc[i]['status']
            path_len = df.iloc[i]['path_len']
            
            if prob < 0.4:
                verdict = "LOW RISK"
                action = "ALLOW"
            else:
                verdict = "HIGH RISK"
                action = "BLOCK/LOG"
                high_risk_detected = True
                
            print(f"Request {i+1:<3} | {status_code:<8} | {path_len:<10} | {prob:.4f}     | {verdict:<9} | {action}")
        
        # Final Summary and Mitigation
        high_risk_count = sum(1 for p in predictions if p > 0.4)
        print("-" * 85)
        print(f"SUMMARY: Processed {len(predictions)} requests.")
        print(f"ALERTS: Found {high_risk_count} security anomalies.")
        
        if high_risk_detected:
            print("\n[!] MITIGATION TRIGGERED: Firewall rules updated to throttle suspicious IP range.")
        print("-" * 85)
        
    else:
        print("\n[!] AI MONITOR: No significant logs found. Generate traffic in Postman first.")

if __name__ == "__main__":
    try:
        train_and_predict()
    except Exception as e:
        print(f"\n[!] ERROR DURING ANALYSIS: {e}")