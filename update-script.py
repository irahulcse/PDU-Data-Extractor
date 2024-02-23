from pysnmp.hlapi import *
from ftplib import FTP
import csv

# Function to fetch data from PDU
def fetch_pdu_data(community, host, port, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            return ' = '.join([x.prettyPrint() for x in varBind])

# Function to write data to a CSV file
def write_to_file(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PDU Data"])
        writer.writerow([data])

# Main function
def main():``
    pdu_data = fetch_pdu_data('community', 'host', 161, 'oid')
    filename = 'pdu_data.csv'
    write_to_file(pdu_data, filename)

if __name__ == "__main__":
    main()