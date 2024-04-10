from pysnmp.hlapi import *
import csv

# Function to fetch data from PDU
def fetch_pdu_data(community, host, port, oids):
    object_types = construct_object_types(oids)

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, port)),
               ContextData(),
               *object_types)
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        data = {}
        for varBind in varBinds:
            oid = varBind[0].prettyPrint()
            value = varBind[1].prettyPrint()
            data[oid] = value
        return data

# Function to construct object types
def construct_object_types(oids):
    object_types = []
    for oid in oids:
        object_types.append(ObjectType(ObjectIdentity(oid)))
    return object_types

# Function to write data to a CSV file
def write_to_file(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PDU Data"])
        writer.writerow([data])

# Main function
def main():
    oids = ['1.3.6.1.2.1.1.7.0', '1.3.6.1.2.1.1.6.0']
    pdu_data = fetch_pdu_data('public', '129.69.80.145', 161, oids)
    filename = 'pdu_data.csv'
    write_to_file(pdu_data, filename)

if __name__ == "__main__":
    main()
