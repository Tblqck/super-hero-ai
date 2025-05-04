import pandas as pd
import os

# Define file paths
files = [
    r"C:\Users\DArK_SIDE\Documents\sporty\predictions_log.csv",
    r"C:\Users\DArK_SIDE\Documents\sporty\rounds_log.csv",
    r"C:\Users\DArK_SIDE\Documents\sporty\state.csv"
]

# Load CSV files into DataFrames
dfs = [pd.read_csv(file) for file in files]

# Standardize column names to lowercase
for df in dfs:
    df.columns = [col.lower() for col in df.columns]

# Merge all DataFrames on 'sequence' column
merged_df = dfs[0]
for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on="sequence", how="outer")

# Convert 'timestamp' column to datetime and find the latest timestamp
merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"], errors='coerce')
latest_timestamp = merged_df["timestamp"].max().strftime("%Y-%m-%d_%H-%M-%S")

# Define output path
output_dir = r"C:\Users\DArK_SIDE\Documents\sporty\model"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
output_file = os.path.join(output_dir, f"merged_{latest_timestamp}.csv")

# Save merged DataFrame
merged_df.to_csv(output_file, index=False)

print(f"Merged file saved as: {output_file}")

# Clear original CSV files, keeping only headers
for file in files:
    df = pd.read_csv(file, nrows=0)  # Read only headers
    df.to_csv(file, index=False)  # Overwrite file with only headers

print("Original CSV files have been cleared, keeping only headers.")
