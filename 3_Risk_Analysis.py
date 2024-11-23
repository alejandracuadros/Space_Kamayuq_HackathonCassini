from pprint import pprint
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

# Load XML files
CDM = {
    "CSPOC": "CSPOC_9.xml",
    "CAESAR_TRJ": "CAESAR_TRJ_12.xml"
}

# Function to parse and extract k   ey data from the XML
def parse_cdm(cdm_path):
    tree = ET.parse(cdm_path)
    root = tree.getroot()

    # Extract fields
    cdm_data = {}

    # Extract fields
    for elem in root.iter():
        tag = elem.tag.split("}")[-1]  # Remove namespace if present
        cdm_data[tag] = elem.text
    return cdm_data


# Parse files
cs_data = parse_cdm(CDM["CSPOC"])
caesar_data = parse_cdm(CDM["CAESAR_TRJ"])

# Combine results for comparison
parsed_data = {
    "CSPOC": cs_data,
    "CAESAR_TRJ": caesar_data
}

"""
    Determine Risk Level: using the TCA from the CDMs and comparing with thresholds.

    ALERT Threshold :
    - Time of Closest Approach <= 7 days.
    - Miss Distance < 5 km and Radial Distance < 500 m, or Probability of Collision > 1E-5.

    WARNING Threshold :
    - Time of Closest Approach <=7 days.
    - Miss Distance < 10 km or Probability of Collision > 1E-6.
"""

# Define thresholds
alert_thresholds = {
    "TCA_days": 7,
    "Miss_Distance_m": 5000,
    "Radial_Distance_m": 500,
    "PoC": 1e-5
}
warning_thresholds = {
    "TCA_days": 7,
    "Miss_Distance_km": 10,
    "PoC": 1e-6
}

def determine_risk_level(data):
    risk_levels = {}

    current_date = datetime.strptime('2023-11-29',"%Y-%m-%d")

    for source, values in data.items():
        try:
            # Extract values
            tca = datetime.strptime(values.get("TCA"), "%Y-%m-%dT%H:%M:%S.%f")
            miss_distance = float(values.get("MISS_DISTANCE", float('inf')))
            radial_distance = float(values.get("RELATIVE_POSITION_R", float('inf')))
            # poc = float(values.get("COLLISION_PROBABILITY", 0))

            days_to_tca = (tca - current_date).days

            # Debugging
            print(f"\nChecking source: {source}")
            print(f"TCA: {tca}, Days to TCA: {days_to_tca}")
            print(f"Miss Distance: {miss_distance} m")
            print(f"Radial Distance: {radial_distance} m")
            # print(f"Collision Probability: {poc}")

            # Threshold logic
            if (
                days_to_tca <= alert_thresholds["TCA_days"]
                and ((miss_distance < alert_thresholds["Miss_Distance_m"]
                      and radial_distance < alert_thresholds["Radial_Distance_m"]))
                     # or poc > alert_thresholds["PoC"])
            ):
                risk_levels[source] = "ALERT"
            elif (
                days_to_tca <= warning_thresholds["TCA_days"]
                and (miss_distance < warning_thresholds["Miss_Distance_m"])
                     # or poc > warning_thresholds["PoC"])
            ):
                risk_levels[source] = "WARNING"
            else:
                risk_levels[source] = "SAFE"

        except (ValueError, TypeError) as e:
            print(f"Error for {source}: {e}")
            risk_levels[source] = "DATA MISSING"

    return risk_levels

risk_levels_ = determine_risk_level(parsed_data)

print("\n Risk levels:")
pprint(risk_levels_)