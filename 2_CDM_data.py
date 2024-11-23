from pprint import pprint
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

# Load XML files
CDM = {
    "CSPOC": "CSPOC_9.xml",
    "CAESAR_TRJ": "CAESAR_TRJ_12.xml"
}

# Function to parse and extract key data from the XML
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

pprint(parsed_data)

# From Dictionary to Dataframe
comparison_table = pd.DataFrame(parsed_data)

print(comparison_table)
