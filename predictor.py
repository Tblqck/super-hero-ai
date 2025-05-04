import numpy as np
import pandas as pd
import onnxruntime as ort
from sklearn.preprocessing import MinMaxScaler
import config

def make_prediction():
    # Load CSV files using correct file paths
    df_test = pd.read_csv(config.PREDICTIONS_LOG)

    if df_test.shape[0] < 12:  # Need at least 12 rows for prediction
        print("⚠️ Not enough data! Need at least 12 rows.")
        return None

    # Ensure 'Sequence' is numeric and sort data from oldest to newest
    df_test['Sequence'] = pd.to_numeric(df_test['Sequence'], errors='coerce')
    df_test = df_test.sort_values(by='Sequence', ascending=True)

    # Select the 12 most recent rows
    df_recent = df_test.tail(12).copy()

    # Scale data safely
    df_recent['Numbers'] = pd.to_numeric(df_recent['Numbers'], errors='coerce')
    scaler = MinMaxScaler()
    
    if df_recent['Numbers'].notnull().sum() > 1:
        df_recent['Scaled Numbers'] = scaler.fit_transform(df_recent[['Numbers']])

    # Prepare X_test
    X_test = df_recent['Scaled Numbers'].values.reshape(1, 12, 1).astype(np.float32)

    # Load model dynamically
    model_path = config.MODEL_PATHS.get(config.MODEL_SELECTION)
    ort_session = ort.InferenceSession(model_path)
    
    input_name = ort_session.get_inputs()[0].name
    predictions = ort_session.run(None, {input_name: X_test})[0]

    if predictions.shape[0] == 0:
        print("⚠️ No predictions were generated!")
        return None

    predicted_class = np.argmax(predictions) + 1  # Convert (0→1, 1→2)

    # Save prediction
    last_sequence = df_test['Sequence'].max()
    next_sequence = last_sequence + 1
    new_entry = pd.DataFrame([[next_sequence, predicted_class]], columns=['Sequence', 'predicted_class'])
    
    try:
        existing_data = pd.read_csv(config.ROUNDS_LOG)
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
    except FileNotFoundError:
        updated_data = new_entry

    updated_data.to_csv(config.ROUNDS_LOG, index=False)
    print(f"✅ Prediction saved: Sequence {next_sequence}, Predicted Class {predicted_class}")

    return predicted_class