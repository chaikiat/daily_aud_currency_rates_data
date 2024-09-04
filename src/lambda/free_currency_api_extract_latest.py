import json
import boto3
import urllib3
import datetime

# REPLACE WITH YOUR DATA FIREHOSE NAME
FIREHOSE_NAME = 'PUT-S3-XXXXX'

def lambda_handler(event, context):
    
    http = urllib3.PoolManager()
    
    r = http.request("GET", "https://api.freecurrencyapi.com/v1/latest?apikey=<api_key>&base_currency=AUD")
    
    # turn it into a dictionary
    r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))
    
    # create a dictionary
    processed_dict = {}

    # Get the current date
    current_date = datetime.datetime.now()
    # extract the other pieces of the dictionary
    processed_dict['day_date'] = current_date.strftime('%Y-%m-%d')
    processed_dict['base_code'] = 'aud'
    processed_dict['bgn'] = r_dict['data']["BGN"]
    processed_dict['brl'] = r_dict['data']['BRL']
    processed_dict['cad'] = r_dict['data']['CAD']
    processed_dict['chf'] = r_dict['data']['CHF']
    processed_dict['cny'] = r_dict['data']['CNY']
    processed_dict['czk'] = r_dict['data']['CZK']
    processed_dict['dkk'] = r_dict['data']['DKK']
    processed_dict['eur'] = r_dict['data']['EUR']
    processed_dict['gbp'] = r_dict['data']['GBP']
    processed_dict['hkd'] = r_dict['data']['HKD']
    processed_dict['hrk'] = r_dict['data']['HRK']
    processed_dict['huf'] = r_dict['data']['HUF']
    processed_dict['idr'] = r_dict['data']['IDR']
    processed_dict['ils'] = r_dict['data']['ILS']
    processed_dict['inr'] = r_dict['data']['INR']
    processed_dict['isk'] = r_dict['data']['ISK']
    processed_dict['jpy'] = r_dict['data']['JPY']
    processed_dict['krw'] = r_dict['data']['KRW']
    processed_dict['mxn'] = r_dict['data']['MXN']
    processed_dict['myr'] = r_dict['data']['MYR']
    processed_dict['nok'] = r_dict['data']['NOK']
    processed_dict['nzd'] = r_dict['data']['NZD']
    processed_dict['php'] = r_dict['data']['PHP']
    processed_dict['pln'] = r_dict['data']['PLN']
    processed_dict['ron'] = r_dict['data']['RON']
    processed_dict['rub'] = r_dict['data']['RUB']
    processed_dict['sek'] = r_dict['data']['SEK']
    processed_dict['sgd'] = r_dict['data']['SGD']
    processed_dict['thb'] = r_dict['data']['THB']
    processed_dict['try'] = r_dict['data']['TRY']
    processed_dict['usd'] = r_dict['data']['USD']
    processed_dict['zar'] = r_dict['data']['ZAR']
    processed_dict['row_ts'] = str(datetime.datetime.now())
    
    # turn it into a string and add a newline
    msg = str(processed_dict) + '\n'
    
    fh = boto3.client('firehose')
    
    reply = fh.put_record(
        DeliveryStreamName=FIREHOSE_NAME,
        Record = {
                'Data': msg
                }
    )

    return reply
