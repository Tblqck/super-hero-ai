import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import RobustScaler
import joblib

def train_and_save_model():
    # Load data from CSV
    data = pd.read_csv("data.csv")
    data = data.sort_values(by="Sequence")  # Ensure data is sorted by Sequence

    # Feature and Target
    X = data["Sequence"].values.reshape(-1, 1)  # Sequence as features
    y = data["Value"].values  # Value as target

    # Use RobustScaler instead of StandardScaler to be more resistant to outliers
    scaler_X = RobustScaler()
    scaler_y = RobustScaler()

    # Apply robust scaling
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

    # Train the model with fine-tuned learning rate
    model = SGDRegressor(max_iter=1000, tol=1e-3, learning_rate="constant", eta0=0.001)
    model.fit(X_scaled, y_scaled)

    # Save the trained model and scalers
    joblib.dump(model, "trained_model.joblib")
    joblib.dump(scaler_X, "scaler_X.joblib")
    joblib.dump(scaler_y, "scaler_y.joblib")

    print("Model trained and saved successfully.")

# Train and save the model by calling the function
train_and_save_model()
