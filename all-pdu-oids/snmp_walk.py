from pysnmp.hlapi import *
import csv

def snmp_walk(community, host, port):
    pdu_data = {}
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData(community),
                              UdpTransportTarget((host, port)),
                              ContextData(),
                              ObjectType(ObjectIdentity('1.3'))):  # Start OID, it will walk through all OIDs

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                oid = varBind[0].prettyPrint()
                value = varBind[1].prettyPrint()
     # Print out the OID so we can see progress
                print(f"Processing {oid}")

                # Save all OIDs, not just ones starting with '1.3.6.1.2.1.1'
                pdu_data[oid] = value

    return pdu_data

def write_to_file(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["OID", "Value"])
        for oid, value in data.items():
            writer.writerow([oid, value])

if __name__ == "__main__":
    pdu_data = snmp_walk('public', '129.69.80.145', 161)
    write_to_file(pdu_data, 'all_pdu_oids.csv')