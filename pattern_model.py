# pattern_model.py

import pandas as pd

def analyze_class_occurrences(df_train, class_sequence):
    df = df_train.copy()
    df['class'] = df['numbers'].apply(lambda x: 1 if x < 5.99 else 2)

    seq_len = len(class_sequence)
    next_class_counts = {1: 0, 2: 0}
    total_matches = 0

    for i in range(len(df) - seq_len):
        window = df['class'].iloc[i:i + seq_len].tolist()
        if window == class_sequence:
            total_matches += 1
            if i + seq_len < len(df):
                next_class = df['class'].iloc[i + seq_len]
                next_class_counts[next_class] += 1

    total_next = sum(next_class_counts.values())
    percent_next_2 = (next_class_counts[2] / total_next * 100) if total_next > 0 else 0
    percent_next_1 = (next_class_counts[1] / total_next * 100) if total_next > 0 else 0

    return {
        "Total_occurrences": total_matches,
        "Percent_next_2": percent_next_2,
        "Percent_next_1": percent_next_1
    }

def pattern_based_prediction(test_data_row, config):
    """
    test_data_row: pd.DataFrame with at least 5 rows (including current one), must include 'numbers', 'sequence'
    config: the config module
    """
    df_train = pd.read_csv(config.PREDICTIONS_LOG)

    if df_train.shape[0] <= 310:
        return 4.0

    df_train = df_train.rename(columns={"Sequence": "sequence", "Numbers": "numbers"})
    test_data_row = test_data_row.rename(columns={"Sequence": "sequence", "Numbers": "numbers"})

    test_data_row['class'] = test_data_row['numbers'].apply(lambda x: 1 if x < 4.99 else 2)

    class_sequence = test_data_row['class'].iloc[-4:].tolist()

    result = analyze_class_occurrences(df_train, class_sequence)

    if result["Total_occurrences"] == 0:
        return 8.0
    elif result["Percent_next_1"] >= 30:
        return 2.0
    else:
        return 1.0