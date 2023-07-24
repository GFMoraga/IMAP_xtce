import pandas as pd
import xml.etree.ElementTree as ET

ET.register_namespace('xtce', "http://www.omg.org/space")

# Load data from Excel file
xls = pd.ExcelFile('/Users/gamo6782/Desktop/IMAP/TLM_COD_20230629-110638(update).xlsx')
sheet_name = "P_COD_HI_INSTRUMENT_COUNTERS"  # Assuming the sheet name is correct
df = xls.parse(sheet_name)

# Fill missing values with '-*-'
df.fillna('-*-', inplace=True)

# Create the root element
root = ET.Element("{http://www.omg.org/space}SpaceSystem", nsmap={"xtce": "http://www.omg.org/space"})
root.attrib["name"] = "P_COD_HI_INSTRUMENT_COUNTERS"

# Create the Header element and its sub-elements
header = ET.SubElement(root, "{http://www.omg.org/space}Header")
header.attrib["date"] = "2023-07-20"
header.attrib["version"] = "1.0"
header.attrib["author"] = "Gabriel Moraga"

# Create the TelemetryMetaData element
telemetry_metadata = ET.SubElement(root, "{http://www.omg.org/space}TelemetryMetaData")

# Create the ParameterTypeSet element
parameter_type_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ParameterTypeSet")

# Create integer parameter types for all numbers between 0-32
for size in range(33):  # Range goes up to 33 to include 0-32
    parameter_type = ET.SubElement(parameter_type_set, "{http://www.omg.org/space}IntegerParameterType")
    parameter_type.attrib["name"] = f"uint{size}"
    parameter_type.attrib["signed"] = "false"

    encoding = ET.SubElement(parameter_type, "{http://www.omg.org/space}IntegerDataEncoding")
    encoding.attrib["sizeInBits"] = str(size)
    encoding.attrib["encoding"] = "unsigned"

    unit_set = ET.SubElement(parameter_type, "{http://www.omg.org/space}UnitSet")

# Create the ParameterSet element
parameter_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ParameterSet")

# Create CCSDS Header parameters. This is the rows 2-8 in the Excel file.
ccsds_parameters = [
    {"name": "VERSION", "parameterTypeRef": "uint3", "description": "CCSDS Packet Version Number (always 0)"},
    {"name": "TYPE", "parameterTypeRef": "uint1", "description": "CCSDS Packet Type Indicator (0=telemetry)"},
    {"name": "SEC_HDR_FLG", "parameterTypeRef": "uint1",
     "description": "CCSDS Packet Secondary Header Flag (always 1)"},
    {"name": "PKT_APID", "parameterTypeRef": "uint11", "description": "CCSDS Packet Application Process ID"},
    {"name": "SEG_FLGS", "parameterTypeRef": "uint2",
     "description": "CCSDS Packet Grouping Flags (3=not part of group)"},
    {"name": "SRC_SEQ_CTR", "parameterTypeRef": "uint14",
     "description": "CCSDS Packet Sequence Count (increments with each new packet)"},
    {"name": "PKT_LEN", "parameterTypeRef": "uint16",
     "description": "CCSDS Packet Length (number of bytes after Packet length minus 1)"}
]

for parameter_data in ccsds_parameters:
    parameter = ET.SubElement(parameter_set, "{http://www.omg.org/space}Parameter")
    parameter.attrib["name"] = parameter_data["name"]
    parameter.attrib["parameterTypeRef"] = parameter_data["parameterTypeRef"]

    description = ET.SubElement(parameter, "{http://www.omg.org/space}LongDescription")
    description.text = parameter_data["description"]

# Create the ContainerSet element
container_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ContainerSet")

# Create the SequenceContainer element
sequence_container = ET.SubElement(container_set, "{http://www.omg.org/space}SequenceContainer")
sequence_container.attrib["name"] = "CCSDSPacket"

# Create the EntryList element and add ParameterRefEntry elements
entry_list = ET.SubElement(sequence_container, "{http://www.omg.org/space}EntryList")
for parameter_data in ccsds_parameters:
    parameter_ref_entry = ET.SubElement(entry_list, "{http://www.omg.org/space}ParameterRefEntry")
    parameter_ref_entry.attrib["parameterRef"] = parameter_data["name"]

# Create the ParameterSet element
parameter_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ParameterSet")

# Process rows from 9 until the last available row in the DataFrame
for index, row in df.iterrows():
    if index < 8:
        continue  # Skip rows before row 9

    # Extract information from the DataFrame row
    mnemonic = row['mnemonic']
    sequence = row['sequence']
    start_byte = row['startByte']
    start_bit_in_byte = row['startBitInByte']
    start_bit = row['startBit']
    length_in_bits = row['lengthInBits']
    data_type = row['dataType']
    convert_as = row['convertAs']
    units = row['units']
    source = row['source']
    short_description = row['shortDescription']
    long_description = row['longDescription']
    mnemonic_length = row['mnemonicLength']

    # Create the Parameter element and its attributes based on the row information
    parameter = ET.SubElement(parameter_set, "{http://www.omg.org/space}Parameter")
    parameter.attrib["name"] = mnemonic
    # Add more attribute assignments based on the row information
    parameter.attrib["sequence"] = str(sequence)
    parameter.attrib["startByte"] = str(start_byte)
    parameter.attrib["startBitInByte"] = str(start_bit_in_byte)
    parameter.attrib["startBit"] = str(start_bit)
    parameter.attrib["lengthInBits"] = str(length_in_bits)
    parameter.attrib["dataType"] = data_type
    parameter.attrib["convertAs"] = convert_as
    parameter.attrib["units"] = units
    parameter.attrib["source"] = source
    parameter.attrib["mnemonicLength"] = str(mnemonic_length)

    description = ET.SubElement(parameter, "{http://www.omg.org/space}LongDescription")

    description.text = long_description

# Create the XML tree
tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)

# Save the XML document to a file
tree.write("P_COD_HI_INSTRUMENT_COUNTERS.xml", encoding="utf-8", xml_declaration=True)
