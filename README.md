
# Setting up PDU Data Extractor


The values that you pass to the fetch_pdu_data function are specific to your PDU and network setup:

'community': This is the community string for SNMP, which acts like a password. It's often set to 'public' by default, but it should be changed to something else for security reasons. You'll need to check your PDU's configuration or documentation to find out what the community string is.

'host': This is the IP address or hostname of your PDU. You should be able to find this in your network configuration or in the PDU's settings.

'port': This is the port number used for SNMP. The default SNMP port is 161.

'oid': This stands for Object Identifier, and it's used in SNMP to identify the specific piece of data you want to fetch from the PDU. The correct OID will depend on what data you want (e.g., current, voltage, power) and will be specified in your PDU's MIB (Management Information Base) or documentation.

Here's an example of how you might call the function with actual values:

pdu_data = fetch_pdu_data('myCommunity', '192.168.1.100', 161, '1.3.6.1.2.1.1.1.0')
In this example, 'myCommunity' is the community string, '192.168.1.100' is the IP address of the PDU, 161 is the SNMP port, and '1.3.6.1.2.1.1.1.0' is an example OID that would fetch the system description from the PDU. Your actual OID will likely be different.