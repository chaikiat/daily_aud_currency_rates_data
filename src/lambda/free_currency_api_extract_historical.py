import json
import boto3
import urllib3
import datetime

# REPLACE WITH YOUR DATA FIREHOSE NAME
FIREHOSE_NAME = 'PUT-S3-XXXXX'

def lambda_handler(event, context):
    
    http = urllib3.PoolManager()
    
    r = http.request("GET", "https://api.freecurrencyapi.com/v1/historical?apikey=<api_key>&date=2024-08-29&base_currency=AUD")
    
    # turn it into a dictionary
    r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))
    
    # extract pieces of the dictionary
    processed_dict = {}
    day_date = list(r_dict['data'].keys())[0]
    processed_dict['day_date'] = day_date
    processed_dict['base_code'] = 'aud'
    processed_dict['bgn'] = r_dict['data'][day_date]["BGN"]
    processed_dict['brl'] = r_dict['data'][day_date]['BRL']
    processed_dict['cad'] = r_dict['data'][day_date]['CAD']
    processed_dict['chf'] = r_dict['data'][day_date]['CHF']
    processed_dict['cny'] = r_dict['data'][day_date]['CNY']
    processed_dict['czk'] = r_dict['data'][day_date]['CZK']
    processed_dict['dkk'] = r_dict['data'][day_date]['DKK']
    processed_dict['eur'] = r_dict['data'][day_date]['EUR']
    processed_dict['gbp'] = r_dict['data'][day_date]['GBP']
    processed_dict['hkd'] = r_dict['data'][day_date]['HKD']
    processed_dict['hrk'] = r_dict['data'][day_date]['HRK']
    processed_dict['huf'] = r_dict['data'][day_date]['HUF']
    processed_dict['idr'] = r_dict['data'][day_date]['IDR']
    processed_dict['ils'] = r_dict['data'][day_date]['ILS']
    processed_dict['inr'] = r_dict['data'][day_date]['INR']
    processed_dict['isk'] = r_dict['data'][day_date]['ISK']
    processed_dict['jpy'] = r_dict['data'][day_date]['JPY']
    processed_dict['krw'] = r_dict['data'][day_date]['KRW']
    processed_dict['mxn'] = r_dict['data'][day_date]['MXN']
    processed_dict['myr'] = r_dict['data'][day_date]['MYR']
    processed_dict['nok'] = r_dict['data'][day_date]['NOK']
    processed_dict['nzd'] = r_dict['data'][day_date]['NZD']
    processed_dict['php'] = r_dict['data'][day_date]['PHP']
    processed_dict['pln'] = r_dict['data'][day_date]['PLN']
    processed_dict['ron'] = r_dict['data'][day_date]['RON']
    processed_dict['rub'] = r_dict['data'][day_date]['RUB']
    processed_dict['sek'] = r_dict['data'][day_date]['SEK']
    processed_dict['sgd'] = r_dict['data'][day_date]['SGD']
    processed_dict['thb'] = r_dict['data'][day_date]['THB']
    processed_dict['try'] = r_dict['data'][day_date]['TRY']
    processed_dict['usd'] = r_dict['data'][day_date]['USD']
    processed_dict['zar'] = r_dict['data'][day_date]['ZAR']
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

