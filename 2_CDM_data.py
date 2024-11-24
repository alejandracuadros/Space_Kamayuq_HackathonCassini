from pprint import pprint
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

# Load XML files
xml_files = {
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
        attributes = elem.attrib
        text = elem.text.strip() if elem.text else None
        cdm_data[tag] = {"value":text, "attributes":text}

    return cdm_data


# Parse files
cs_data = parse_cdm(xml_files["CSPOC"])
caesar_data = parse_cdm(xml_files["CAESAR_TRJ"])

# Combine results for comparison
parsed_data = {
    "CSPOC": cs_data,
    "CAESAR_TRJ": caesar_data
}

pprint(parsed_data)

# From Dictionary to Dataframe
# comparison_table = pd.DataFrame(parsed_data)
#
# print(comparison_table)


import xml.etree.ElementTree as ET
from pprint import pprint

# Function to parse and organize data from CDM XML content
def parse_cdm_data(xml_content):
    try:
        # Parse XML from string
        root = ET.fromstring(xml_content)

        # Initialize structured data
        cdm_data = {
            "general": {},
            "object1": {},
            "object2": {}
        }

        # Extract general data
        for elem in root.findall(".//relativeMetadataData/*"):
            tag = elem.tag.split("}")[-1]
            attributes = elem.attrib
            value = elem.text.strip() if elem.text else None
            cdm_data["general"][tag] = {"value": value, "attributes": attributes}

        # Extract OBJECT1 data
        for elem in root.findall(".//segment/metadata"):
            if elem.find("OBJECT").text == "OBJECT1":
                for sub_elem in elem:
                    tag = sub_elem.tag.split("}")[-1]
                    attributes = sub_elem.attrib
                    value = sub_elem.text.strip() if sub_elem.text else None
                    cdm_data["object1"][tag] = {"value": value, "attributes": attributes}

        # Extract OBJECT2 data
        for elem in root.findall(".//segment/metadata"):
            if elem.find("OBJECT").text == "OBJECT2":
                for sub_elem in elem:
                    tag = sub_elem.tag.split("}")[-1]
                    attributes = sub_elem.attrib
                    value = sub_elem.text.strip() if sub_elem.text else None
                    cdm_data["object2"][tag] = {"value": value, "attributes": attributes}

        return cdm_data
    except Exception as e:
        return {"error": str(e)}

# XML contents for both CDMs
csxml_content = """<?xml version="1.0" encoding="ISO-8859-1"?><cdm xmlns:ndm="urn:ccsds:recommendation:navigation:schema:ndmxml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="CCSDS_CDM_VERS" version="1.0" xsi:noNamespaceSchemaLocation="http://sanaregistry.org/r/ndmxml/ndmxml-1.0-master.xsd"><header><COMMENT>CDM_ID:611215496</COMMENT><COMMENT>EVENT_ID:CA-24001A-90094A-202312021836</COMMENT><CREATION_DATE>2023-11-26T02:06:03.000</CREATION_DATE><ORIGINATOR>CSpOC</ORIGINATOR><MESSAGE_FOR>SAT_1</MESSAGE_FOR><MESSAGE_ID>000000001E_conj_000020923_2023336183714_330020518260</MESSAGE_ID></header><body><relativeMetadataData><TCA>2023-12-02T18:37:14.815</TCA><MISS_DISTANCE units="m">4996.945216829978</MISS_DISTANCE><RELATIVE_SPEED units="m/s">725.3052185114899</RELATIVE_SPEED><relativeStateVector><RELATIVE_POSITION_R units="m">345.0</RELATIVE_POSITION_R><RELATIVE_POSITION_T units="m">4949.9</RELATIVE_POSITION_T><RELATIVE_POSITION_N units="m">590.7</RELATIVE_POSITION_N><RELATIVE_VELOCITY_R units="m/s">-0.9</RELATIVE_VELOCITY_R><RELATIVE_VELOCITY_T units="m/s">-85.9</RELATIVE_VELOCITY_T><RELATIVE_VELOCITY_N units="m/s">720.2</RELATIVE_VELOCITY_N></relativeStateVector></relativeMetadataData><segment><metadata><OBJECT>OBJECT1</OBJECT><OBJECT_DESIGNATOR>00001</OBJECT_DESIGNATOR><OBJECT_NAME>SAT_1</OBJECT_NAME><MANEUVERABLE>NO</MANEUVERABLE></metadata></segment></body></cdm>"""

caesarxml_content = """<?xml version="1.0" encoding="ISO-8859-1"?><cdm xmlns:ndm="urn:ccsds:recommendation:navigation:schema:ndmxml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="CCSDS_CDM_VERS" version="1.0" xsi:noNamespaceSchemaLocation="http://sanaregistry.org/r/ndmxml/ndmxml-1.0-master.xsd"><header><COMMENT>Secondary = CDM: CSpOC.14_33201115511 (TCA: 02/12/2023 18:37:14.848Z)</COMMENT><COMMENT>EVENT_ID:CA-24001A-90094A-202312021836</COMMENT><CREATION_DATE>2023-11-28T02:22:38.815</CREATION_DATE><ORIGINATOR>CAESAR</ORIGINATOR><MESSAGE_FOR>SAT_1</MESSAGE_FOR><MESSAGE_ID>TRJ18806328</MESSAGE_ID></header><body><relativeMetadataData><TCA>2023-12-02T18:37:14.777</TCA><MISS_DISTANCE units="m">4772.359683969186</MISS_DISTANCE><RELATIVE_SPEED units="m/s">725.2699170401662</RELATIVE_SPEED><relativeStateVector><RELATIVE_POSITION_R units="m">344.90742025190144</RELATIVE_POSITION_R><RELATIVE_POSITION_T units="m">4726.382735102276</RELATIVE_POSITION_T><RELATIVE_POSITION_N units="m">563.7038814455515</RELATIVE_POSITION_N></relativeStateVector></relativeMetadataData><segment><metadata><OBJECT>OBJECT1</OBJECT><OBJECT_NAME>SAT_1</OBJECT_NAME><MANEUVERABLE>YES</MANEUVERABLE></metadata></segment></body></cdm>"""

# Parse both XMLs
cs_data_parsed = parse_cdm_data(csxml_content)
caesar_data_parsed = parse_cdm_data(caesarxml_content)

# Display the results
print("\nCSpOC Parsed Data:")
pprint(cs_data_parsed)

print("\nCAESAR Parsed Data:")
pprint(caesar_data_parsed)
