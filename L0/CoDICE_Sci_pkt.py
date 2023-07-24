import xml.etree.ElementTree as ET
ET.register_namespace('xtce', "http://www.omg.org/space")

# Create the root element
root = ET.Element("{http://www.omg.org/space}SpaceSystem")
root.attrib["name"] = "CoDICE_Science_Pkt"

# Create the Header element and its attributes
header = ET.SubElement(root, "{http://www.omg.org/space}Header")
header.attrib["date"] = "2023-06-20"
header.attrib["version"] = "1.0"
header.attrib["author"] = "Gabriel Moraga"

# Create the TelemetryMetaData element
telemetry_metadata = ET.SubElement(root, "{http://www.omg.org/space}TelemetryMetaData")

# Create the ParameterTypeSet element
parameter_type_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ParameterTypeSet")

# Create integer parameter types
integer_sizes = [1, 2, 3, 4, 11, 12, 14, 16, 20, 32]
for size in integer_sizes:
    parameter_type = ET.SubElement(parameter_type_set, "{http://www.omg.org/space}IntegerParameterType")
    parameter_type.attrib["name"] = f"uint{size}"
    parameter_type.attrib["signed"] = "false"

    encoding = ET.SubElement(parameter_type, "{http://www.omg.org/space}IntegerDataEncoding")
    encoding.attrib["sizeInBits"] = str(size)
    encoding.attrib["encoding"] = "unsigned"

    unit_set = ET.SubElement(parameter_type, "{http://www.omg.org/space}UnitSet")

# Create the ParameterSet element
parameter_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ParameterSet")

# Create CoDICE Science Packet parameters
codice_parameters = [
    {"name": "Packet_Version", "parameterTypeRef": "unit16", "description": "Packet Version"},
    {"name": "Spare", "parameterTypeRef": "unit16", "description": "Spare for alignment"},
    {"name": "Acq_Start_Seconds", "parameterTypeRef": "unit32", "description": "Acquisition Start Time (Seconds)"},
    {"name": "Acq_Start_Subseconds", "parameterTypeRef": "unit20", "description": "Acquisition Start Time (Subseconds)"},
    {"name": "Counter_ID", "parameterTypeRef": "unit12", "description": "Counter ID"},
    {"name": "Table_ID", "parameterTypeRef": "unit32", "description": "Science Lookup Table Version/ID"},
    {"name": "Plan_ID", "parameterTypeRef": "unit16", "description": "Plan Table ID"},
    {"name": "Plan_Step", "parameterTypeRef": "unit4", "description": "Plan Step Number"},
    {"name": "View_ID", "parameterTypeRef": "unit4", "description": "View table used for data collapsing and compression"},
    {"name": "RGFO_Half_Spin", "parameterTypeRef": "unit4", "description": "Half-spin when Reduced Gain Factor Operation was activated"},
    {"name": "NSO_Half_Spin", "parameterTypeRef": "unit4", "description": "Half-spin when No Scan Operation was activated"},
    {"name": "Spare0", "parameterTypeRef": "unit8", "description": "Spare for alignment"},
    {"name": "Bias_Gain_Mode", "parameterTypeRef": "unit1", "description": "Bias Voltage Mode"},
    {"name": "Suspect", "parameterTypeRef": "unit1", "description": "Indicates a data quality issue"},
    {"name": "Compression", "parameterTypeRef": "unit2", "description": "Compression Configuration"},
    {"name": "Byte_Count", "parameterTypeRef": "unit20", "description": "Number of bytes in the Data array"}
]

for parameter_data in codice_parameters:
    parameter = ET.SubElement(parameter_set, "{http://www.omg.org/space}Parameter")
    parameter.attrib["name"] = parameter_data["name"]
    parameter.attrib["parameterTypeRef"] = parameter_data["parameterTypeRef"]

    description = ET.SubElement(parameter, "{http://www.omg.org/space}LongDescription")
    description.text = parameter_data["description"]

# Create the ContainerSet element
container_set = ET.SubElement(telemetry_metadata, "{http://www.omg.org/space}ContainerSet")

# Create the SequenceContainer element
sequence_container = ET.SubElement(container_set, "{http://www.omg.org/space}SequenceContainer")
sequence_container.attrib["name"] = "CoDICE_Science_Pkt"

# Create the EntryList element and add ParameterRefEntry elements
entry_list = ET.SubElement(sequence_container, "{http://www.omg.org/space}EntryList")
entry_params = ["SHCOARSE", "Packet_Version", "Spare", "Acq_Start_Seconds", "Acq_Start_Subseconds",
                "Counter_ID", "Table_ID", "Plan_ID", "Plan_Step", "View_ID", "RGFO_Half_Spin",
                "NSO_Half_Spin", "Spare0", "Bias_Gain_Mode", "Suspect", "Compression", "Byte_Count", "Data"]
for parameter in entry_params:
    parameter_ref_entry = ET.SubElement(entry_list, "{http://www.omg.org/space}ParameterRefEntry")
    parameter_ref_entry.attrib["parameterRef"] = parameter

# Create the XML tree
tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)

# Save the XML document to a file
tree.write("CoDICE_Science_Pkt.xml", encoding="utf-8", xml_declaration=True)
