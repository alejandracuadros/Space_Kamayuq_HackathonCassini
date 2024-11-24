import pandas as pd
from datetime import datetime
from pprint import pprint

# Load the provided CSV files for the most reliable entries
cspoc_file = "cdm_cspoc_results/most_reliable_entry_cspoc.csv"
trj_file = "cdm_caesar_trj_results/most_reliable_entry_caesar_trj.csv"
alm_file = "cdm_caesar_alm_results/most_reliable_entry_caesar_alm.csv"

# Read the CSV files into pandas DataFrames
cspoc_data = pd.read_csv(cspoc_file)
trj_data = pd.read_csv(trj_file)
alm_data = pd.read_csv(alm_file)

# Function to restructure the key-value pair format into a proper DataFrame
def clean_csv_data(data):
    # Set the first column as the key, transpose, and reset the index to create a clean DataFrame
    key_value_pairs = data.set_index(data.columns[0]).T
    key_value_pairs.reset_index(drop=True, inplace=True)
    return key_value_pairs

# Clean the three datasets
cspoc_cleaned = clean_csv_data(cspoc_data)
trj_cleaned = clean_csv_data(trj_data)
alm_cleaned = clean_csv_data(alm_data)

# Combine the cleaned data for analysis
reliable_entries_cleaned = pd.concat([cspoc_cleaned, trj_cleaned, alm_cleaned], ignore_index=True)

# Parse dates and ensure numeric fields are correctly formatted
reliable_entries_cleaned['Metadata_TCA'] = pd.to_datetime(reliable_entries_cleaned['Metadata_TCA'], errors='coerce')
reliable_entries_cleaned['Metadata_MISS_DISTANCE'] = pd.to_numeric(reliable_entries_cleaned['Metadata_MISS_DISTANCE'], errors='coerce')
reliable_entries_cleaned['Metadata_RELATIVE_POSITION_R'] = pd.to_numeric(
    reliable_entries_cleaned['Metadata_relativeStateVector_RELATIVE_POSITION_R'], errors='coerce'
)

# Define thresholds for risk levels
alert_thresholds = {
    "TCA_days": 7,
    "Miss_Distance_m": 5000,
    "Radial_Distance_m": 500,
    "PoC": 1e-5
}
warning_thresholds = {
    "TCA_days": 7,
    "Miss_Distance_m": 10000,
    "PoC": 1e-6
}

# Function to determine risk level
def determine_risk_level(row, current_date):
    try:
        tca = row['Metadata_TCA']
        miss_distance = row['Metadata_MISS_DISTANCE']
        radial_distance = row['Metadata_RELATIVE_POSITION_R']
        # poc = float(row.get('COLLISION_PROBABILITY', 0))  # Uncomment if PoC is present

        days_to_tca = (tca - current_date).days

        if (
            days_to_tca <= alert_thresholds["TCA_days"]
            and (miss_distance < alert_thresholds["Miss_Distance_m"]
                 and radial_distance < alert_thresholds["Radial_Distance_m"])
            # or poc > alert_thresholds["PoC"]  # Uncomment if PoC is available
        ):
            return "ALERT"
        elif (
            days_to_tca <= warning_thresholds["TCA_days"]
            and miss_distance < warning_thresholds["Miss_Distance_m"]
            # or poc > warning_thresholds["PoC"]  # Uncomment if PoC is available
        ):
            return "WARNING"
        else:
            return "SAFE"
    except Exception as e:
        return "DATA MISSING"


# Current date for comparison
current_date = datetime.strptime("2023-11-29", "%Y-%m-%d")

# Apply risk determination to each entry
reliable_entries_cleaned['Risk_Level'] = reliable_entries_cleaned.apply(lambda row: determine_risk_level(row, current_date), axis=1)

# Display the results with risk levels
risk_level_results = reliable_entries_cleaned[['FileName', 'Metadata_TCA', 'Metadata_MISS_DISTANCE', 'Metadata_RELATIVE_POSITION_R', 'Risk_Level']]
print("\n--- Risk Levels for Most Reliable Entries ---")
print(risk_level_results)

# Save the results to a CSV file
output_file = "risk_level_results_combined.csv"
risk_level_results.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")
