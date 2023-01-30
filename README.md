# CSV2SEPA-XML-Converter
Transform your CSV transactions into SEPA XML with ease

This script generates a valid SEPA XML file for direct debit transactions from a CSV file supplied by the user. This can be useful for making many transactions from the same bank account, as it allows for the creation of a batch transfer SEPA XML file that can be uploaded to a bank or banking tool, such as MoneyMoney. This is much quicker than creating transactions individually.

### Getting Started
To get started using the script, you will need to do the following:

1. Replace the values in the config.ini file with the name, IBAN, and BIC of the account from which the money is being sent.
2. Provide a CSV file that contains the following rows: *Creditor_Name, Creditor_IBAN, Creditor_BIC, Remittance_Info, Payment_Amount*.

A template CSV called 'transactions-template.csv' is included in the repository for convenience.

### Usage
To use the script, simply run the following command in your terminal:

```
python3 csv-to-sepa_xml.py [path to CSV file]
```
The script will then generate a SEPA XML file in the same directory as the provided CSV file.

#### Obligatory Disclaimer
*It is important to note that the use of this script is at your own risk. I am not responsible for any mishaps that may occur when using a generated XML. It is your responsibility to ensure that the information provided in the config.ini file and the CSV file is accurate and that the generated XML file does what you want it to do. :)*
