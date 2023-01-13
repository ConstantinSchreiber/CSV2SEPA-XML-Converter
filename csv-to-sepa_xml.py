import csv
import xml.etree.ElementTree as ET
import sys
import os
import string
import random
from datetime import datetime
import configparser

def current_time_date():
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    return current_time

def generate_payment_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(32))

def generate_sepa(csv_file, debitor_name, debitor_iban, debitor_bic):

    controlSum = 0
    numOfTx = 0
    

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)

        # Create the root element for the SEPA XML
        sepa = ET.Element('Document')
        sepa.set('xmlns', "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03")
        
        CstmrCdtTrfInitn = ET.SubElement(sepa,'CstmrCdtTrfInitn')
        GrpHdr = ET.SubElement(CstmrCdtTrfInitn,'GrpHdr')

        # Generates random payment id 
        MsgId = ET.SubElement(GrpHdr,'MsgId')
        MsgId.text = generate_payment_id()

        # Use current time and date as creditor time
        CreDtTm = ET.SubElement(GrpHdr,'CreDtTm')
        CreDtTm.text = current_time_date()

        InitgPty = ET.SubElement(GrpHdr,'InitgPty')

        Nm = ET.SubElement(InitgPty,'Nm')
        Nm.text = debitor_name.upper()


        
        for row in reader:
            PmtInf = ET.SubElement(CstmrCdtTrfInitn,'PmtInf')
            PmtId = ET.SubElement(PmtInf,'PmtId')
            InstrId = ET.SubElement(PmtId,'InstrId')
            InstrId.text = row['Remittance_Info']
            EndToEndId = ET.SubElement(PmtId,'EndToEndId')
            EndToEndId.text = row['Remittance_Info']
            
   
            
            Dbtr = ET.SubElement(PmtInf,'Dbtr')
            Nm = ET.SubElement(Dbtr,'Nm')
            Nm.text = debitor_name
            
            DbtrAcct = ET.SubElement(PmtInf,'DbtrAcct')
            Id = ET.SubElement(DbtrAcct,'Id')
            IBAN = ET.SubElement(Id,'IBAN')
            IBAN.text = debitor_iban
            
            DbtrAgt = ET.SubElement(PmtInf,'DbtrAgt')
            FinInstnId = ET.SubElement(DbtrAgt,'FinInstnId')
            BIC = ET.SubElement(FinInstnId,'BIC')
            BIC.text = debitor_bic

            numOfTx += 1 

            CdtTrfTxInf = ET.SubElement(PmtInf,'CdtTrfTxInf')

            Amt = ET.SubElement(CdtTrfTxInf,'Amt')

            InstdAmt = ET.SubElement(Amt,'InstdAmt', Ccy='EUR')
            InstdAmt.text = row['Payment_Amount']
            controlSum += float(row['Payment_Amount'])

            Cdtr = ET.SubElement(CdtTrfTxInf,'Cdtr')

            Nm = ET.SubElement(Cdtr,'Nm')
            Nm.text = row['Creditor_Name']
            
            CdtrAcct = ET.SubElement(CdtTrfTxInf,'CdtrAcct')
            Id = ET.SubElement(CdtrAcct,'Id')
            IBAN = ET.SubElement(Id,'IBAN')
            IBAN.text = row['Creditor_IBAN']
            
            CdtrAgt = ET.SubElement(CdtTrfTxInf,'CdtrAgt')
            FinInstnId = ET.SubElement(CdtrAgt,'FinInstnId')
            BIC = ET.SubElement(FinInstnId,'BIC')
            BIC.text = row['Creditor_BIC']
            
            RmtInf = ET.SubElement(CdtTrfTxInf,'RmtInf')
            Ustrd = ET.SubElement(RmtInf,'Ustrd')
            Ustrd.text = row['Remittance_Info']


        # Store number of transactions
        NbOfTxs = ET.SubElement(GrpHdr,'Nb0fTxs')
        NbOfTxs.text = str(numOfTx)

        # Control sum (total transfer amount)
        CtrlSum = ET.SubElement(GrpHdr,'MsgId')
        CtrlSum.text = str(controlSum)
            
        # Create the SEPA XML string
        sepa_xml = ET.tostring(sepa, encoding='unicode')

    # Save the SEPA XML to a file in the same directory as the CSV file
    filename, file_extension = os.path.splitext(csv_file)
    sepa_xml_file = filename + '.xml'
    with open(sepa_xml_file, 'w') as f:
        f.write(sepa_xml)


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'DEBITOR' not in config or not all(config.get('DEBITOR', x) for x in ['Debitor_Name', 'Debitor_IBAN', 'Debitor_BIC']):
        print("One or more of the required values are missing or empty in config.ini. Please add Debitor_Name, Debitor_IBAN, Debitor_BIC in [DEBITOR] section.")
        sys.exit(1)
    elif len(sys.argv) < 2:
        print('Please provide the path to the CSV file')
        sys.exit(1)

    csv_file = sys.argv[1]
    debitor_name = config.get('DEBITOR', 'Debitor_Name')
    debitor_iban = config.get('DEBITOR', 'Debitor_IBAN')
    debitor_bic = config.get('DEBITOR', 'Debitor_BIC')

    generate_sepa(csv_file, debitor_name, debitor_iban, debitor_bic )
