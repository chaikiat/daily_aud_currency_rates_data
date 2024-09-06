import sys
import awswrangler as wr
import logging

# enable logging of data quality check results to AWS Cloudwatch
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# check 1: check that row count between the source (non-parquet) table matches with the transformed (parquet) table
ROW_COUNT_DQ_CHECK = f"""
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM "de_proj_database"."de_aug_source_data_currency") - (SELECT COUNT(*) FROM "de_proj_database"."free_currency_aud_data_parquet_tbl") <> 0 
        THEN 1 
        ELSE 0 
    END AS res_col
;
"""

# check 2: check for NULL values in the rows for myr column, if NULL values exist then return an integer > 0
NULL_DQ_CHECK = f"""
SELECT 
    SUM(CASE WHEN myr IS NULL THEN 1 ELSE 0 END) AS res_col
FROM "de_proj_database"."free_currency_aud_data_parquet_tbl";
"""

# check 3: check for percentage rate of NULL values in the rows for myr column to enable a buffer for NULL values from the source data, set to zero threshold as default
NULL_PERCENT_DQ_CHECK : f"""
SELECT
     SUM(CASE WHEN myr IS NULL THEN 1 ELSE 0 END) AS cnt_null_myr
    ,SUM(CASE WHEN myr IS NULL THEN 1 ELSE 0 END) * 1.0 / (SELECT COUNT(*) FROM "de_proj_database"."free_currency_aud_data_parquet_tbl") AS res_col
FROM "de_proj_database"."free_currency_aud_data_parquet_tbl";
"""

# check 4: check for any duplicate rows, if duplicate rows exist then return an integer > 0

DUPLICATE_DQ_CHECK = f"""
SELECT
     day_date
     ,base_code
    ,COUNT(*) AS res_col
FROM "de_proj_database"."free_currency_aud_data_parquet_tbl"
GROUP BY 1,2
HAVING COUNT(*) > 1
;
"""

# define function to run the quality checks

def dq_check(query, dq_check_task):
    try:
        df = wr.athena.read_sql_query(sql=query, database="de_proj_database")

# exit if we get a result > 0
        if df['res_col'][0] > 0:
            logger.error(f'{dq_check_task} returned results. This data quality check has failed.')
            sys.exit(1)
        else:
            print('Quality check passed.')
            logger.info(f'{dq_check_task} quality check has passed.')
# log exceptions
    except Exception as e:  
        logger.error(f'There was an error while running {dq_check_task}: {str(e)}')
        sys.exit(1)
    
# Execute each data quality check task in sequence
    dq_check(ROW_COUNT_DQ_CHECK, "ROW_COUNT_DQ_CHECK")
    dq_check(NULL_DQ_CHECK, "NULL_DQ_CHECK")
    dq_check(NULL_PERCENT_DQ_CHECK, "NULL_PERCENT_DQ_CHECK")
    dq_check(DUPLICATE_DQ_CHECK, "DUPLICATE_DQ_CHECK")

# Log that all data quality checks has passed
logger.info('All data quality checks have passed successfully.')


