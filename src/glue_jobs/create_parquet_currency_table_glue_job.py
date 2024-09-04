import sys
import boto3

client = boto3.client('athena')

SOURCE_TABLE_NAME = 'de_aug_source_data_currency'
NEW_TABLE_NAME = 'free_currency_aud_data_parquet_tbl'
NEW_TABLE_S3_BUCKET = 's3://free-currency-aud-data-parquet-bucket-ck/'
MY_DATABASE = 'de_proj_database'
QUERY_RESULTS_S3_BUCKET = 's3://query-results-location-de-proj-currency'

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    CREATE TABLE {NEW_TABLE_NAME} WITH
    (external_location='{NEW_TABLE_S3_BUCKET}',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['row_ts'])
    AS

    SELECT
        day_date
        ,base_code
        ,bgn,brl,cad,chf,cny,czk,dkk,eur,gbp,hkd,hrk,huf,idr,ils,inr,isk,jpy,krw,mxn,myr,nok,nzd,php,pln,ron,rub,sek,sgd,thb,try,usd,zar
        ,row_ts
    FROM "{MY_DATABASE}"."{SOURCE_TABLE_NAME}"

    ;
    """,
    QueryExecutionContext = {
        'Database': f'{MY_DATABASE}'
    }, 
    ResultConfiguration = { 'OutputLocation': f'{QUERY_RESULTS_S3_BUCKET}'}
)

# list of responses
resp = ["FAILED", "SUCCEEDED", "CANCELLED"]

# get the response
response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])

# wait until query finishes
while response["QueryExecution"]["Status"]["State"] not in resp:
    response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])
    
# if it fails, exit and give the Athena error message in the logs
if response["QueryExecution"]["Status"]["State"] == 'FAILED':
    sys.exit(response["QueryExecution"]["Status"]["StateChangeReason"])
