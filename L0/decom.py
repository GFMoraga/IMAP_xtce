from space_packet_parser import parser, xtcedef

def decom_packets(packet_file: str, xtce_packet_definition: str) -> list:
    """Unpack CCSDS data packet. In this function, we unpack and return data
    as it is. Data modification will not be done at this step.

    Parameters
    ----------
    packet_file : str
        Path to data packet path with filename
    xtce_packet_definition : str
        Path to XTCE file with filename

    Returns
    -------
    List
        List of all the unpacked data

    If the XTCE file is not valid, an empty list will be returned and an error message will be printed.
    """
    try:
        packet_definition = xtcedef.XtcePacketDefinition(xtce_packet_definition)
    except Exception as e:
        print(f"Error loading XTCE definition: {e}")
        return []

    packet_parser = parser.PacketParser(packet_definition)

    with open(packet_file, "rb") as binary_data:
        packet_generator = packet_parser.generator(binary_data)
        return list(packet_generator)

# Paths to your binary data file and XTCE file
binary_data_file = "path/to/your/binary/data.bin"
xtce_file = "path/to/your/xtce/file.xml"

print(f"XTCE File: {xtce_file}")
# Call the function to parse the binary data
unpacked_data = decom_packets(binary_data_file, xtce_file)

# Now you can work with the unpacked data, which will be a list of parsed packets.
# For example, you can print the parsed packets:
for packet in unpacked_data:
    print(packet)
