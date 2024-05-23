from pysnmp.hlapi import *
import csv
import time
from prometheus_client import start_http_server, Gauge

# define a gauge metric to represent PDU data
PDU_GAUGE = Gauge('pdu_data', 'Data fetched from PDU', ['oid'])

# function to fetch data from PDU
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
                    value_str = varBind[1].prettyPrint()
                    value = float(value_str.replace(' kWh', ''))
                    data[oid] = value
                    print(f"Fetched data: {oid} = {value}")  
                    PDU_GAUGE.labels(oid=oid).set(value)
                print("Data fetched successfully.")
                return data
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

def construct_object_types(oids):
    object_types = []
    for oid in oids:
        object_types.append(ObjectType(ObjectIdentity(oid)))
    return object_types
# function to write data to a CSV file
def write_to_file(data, filename):
    with open(filename, 'a', newline='') as file:  # 'a' for append mode
        writer = csv.writer(file)
        for oid, value in data.items():
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), f"{oid}: {value}"])  # add timestamp
    print(f"Data written to {filename}.")

# function to clear the CSV file
def clear_file(filename):
    with open(filename, 'w') as file:
        pass  # do nothing
    print(f"Data in {filename} cleared.")

# main function
def main():
    # start up the server to expose the metrics.
    start_http_server(8000)
    oids=['1.3.6.1.4.1.2606.7.4.2.2.1.10.2.85']  # replace with new OID
    filename = 'pdu_data.csv'
    
    last_clear_time = time.time()  # record when the file was last cleared

    while True:
        pdu_data = fetch_pdu_data('public', '129.69.80.130', 161, oids)
        write_to_file(pdu_data, filename)

        # check if a week has passed since the last time the file was cleared
        if time.time() - last_clear_time >= 7 * 24 * 60 * 60:  # 7 days * 24 hours/day * 60 minutes/hour * 60 seconds/minute
            clear_file(filename)
            last_clear_time = time.time()  # update the last clear time

        time.sleep(5)

if __name__ == "__main__":
    main()