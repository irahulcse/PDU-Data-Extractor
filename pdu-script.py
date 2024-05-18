from pysnmp.hlapi import *
import csv
import time

# Function to fetch data from PDU
def fetch_pdu_data(community, host, port, oids):
    object_types = construct_object_types(oids)

    while True:
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((host, port)),
                       ContextData(),
                       *object_types)
            )

            if errorIndication:
                print(errorIndication)
                time.sleep(5)
                continue
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                time.sleep(5)
                continue
            else:
                data = {}
                for varBind in varBinds:
                    oid = varBind[0].prettyPrint()
                    value = varBind[1].prettyPrint()
                    data[oid] = value
                print("Data fetched successfully.")
                return data
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

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
        for oid, value in data.items():
            writer.writerow([f"{oid}: {value}"])
    print(f"Data written to {filename}.")

# Main function
def main():
    oids=['1.3.6.1.4.1.2606.7.4.2.2.1.10.2.85']
    filename = 'pdu_data.csv'
    
    while True:
        pdu_data = fetch_pdu_data('public', '129.69.80.130', 161, oids)
        write_to_file(pdu_data, filename)
        time.sleep(5)

if __name__ == "__main__":
    main()