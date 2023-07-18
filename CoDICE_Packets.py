''' This the sheet called "Packets" in the provided Excel file. It contains
    the packet name, APID, extended ID, and max length in bits. The APID is
    converted to hex and the extended ID is converted to a string. The max
    length is used to determine the size of the parameter type. The packet name
    is the specific name of the packet. The extended ID is not given at this time
    '''

import pandas as pd
import xml.etree.ElementTree as ET

ET.register_namespace('xtce', "http://www.omg.org/space")

# Read the Excel file
''' This example is pulled from my local, but in the future it will be pulled from the cloud or gateway. 
    The sheet name is the name of the sheet in the Excel file. The sheet name is used to create the
    root element. The sheetname can be changed to whatever the user wants.
    '''
xls = pd.ExcelFile('/Users/gamo6782/Desktop/COD_TLM_20230316-175906.xlsx')
sheet_name = xls.sheet_names[1]  # Assuming 'Packets' is the second sheet
df = xls.parse(sheet_name)

# Fill empty cells in the 'extendedid' column with "N/A"
df['extendedid'].fillna('N/A', inplace=True)

# Create the root element
root = ET.Element("{http://www.omg.org/space}SpaceSystem", nsmap={"xtce": "http://www.omg.org/space"})
root.attrib["name"] = "Packets"

# Create the Header element and its sub-elements
header = ET.SubElement(root, "{http://www.omg.org/space}Header")
header.attrib["date"] = "2023-06-20"
header.attrib["version"] = "1.0"
header.attrib["author"] = "Gabriel Moraga"

# Create the TelemetryMetaData element
telemetry_metadata = ET.SubElement(root, "{http://www.omg.org/space}TelemetryMetaData")

# Create the ParameterTypeSet element
parameter_type_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ParameterTypeSet")

# Iterate over the rows of the sheet
for _, row in df.iterrows():
    packet_name = row['packetName']
    ap_id_hex = row['apIdHex']
    extended_id = row['extendedid']
    max_length_bits = row['maxLengthBits']

    # Create the Packet element
    packet_element = ET.SubElement(parameter_type_set, "{http://www.omg.org/space}Packet")
    packet_element.attrib["packetName"] = packet_name

    # Create the apIdHex element
    ap_id_hex_element = ET.SubElement(packet_element, "{http://www.omg.org/space}apIdHex")
    ap_id_hex_element.text = ap_id_hex

    # Create the extendedid element
    extended_id_element = ET.SubElement(packet_element, "{http://www.omg.org/space}extendedid")
    extended_id_element.text = str(extended_id)

    # Create the maxLengthBits element
    max_length_bits_element = ET.SubElement(packet_element, "{http://www.omg.org/space}maxLengthBits")
    max_length_bits_element.text = str(max_length_bits)

# Create the XML tree
tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)
# Save the XML document to a file
tree.write('Packets.xml', encoding='utf-8', xml_declaration=True)
