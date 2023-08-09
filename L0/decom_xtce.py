from pathlib import Path
from space_packet_parser import parser, xtcedef



# Define paths
packet_file = Path('/Users/gamo6782/Desktop/RAW.bin')
xtce_document = Path('/Users/gamo6782/Desktop/IMAP_xtce/xtce_repo/L0/p_cod_aut_def.xml')

packet_definition = xtcedef.XtcePacketDefinition(xtce_document)
my_parser = parser.PacketParser(packet_definition)

with packet_file.open('rb') as binary_data:
    packet_generator = my_parser.generator(binary_data)

    for packet in packet_generator:
        # Do something with the packet data
        print(packet.header['PKT_APID'])
        print(packet.data)


