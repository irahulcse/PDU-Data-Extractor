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

# Function to upload file to FTP server
def upload_to_ftp(filename, ftp_host, ftp_user, ftp_pass):
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)
    
    with open(filename, 'rb') as fp:
        ftp.storbinary('STOR %s' % filename, fp)

    ftp.quit()

# Main function
def main():
    pdu_data = fetch_pdu_data('community', 'host', 161, 'oid')
    filename = 'pdu_data.csv'
    write_to_file(pdu_data, filename)
    upload_to_ftp(filename, 'your_ftp_host', 'your_ftp_username', 'your_ftp_password')

if __name__ == "__main__":
    main()