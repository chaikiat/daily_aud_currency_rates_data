import sys
import awswrangler as wr

# this check counts the number of NULL rows in the myr column
# if any rows are NULL, the check returns a number > 0
NULL_DQ_CHECK = f"""
SELECT 
    SUM(CASE WHEN myr IS NULL THEN 1 ELSE 0 END) AS myr_col
FROM "de_proj_database"."free_currency_aud_data_parquet_tbl"
;
"""

# run the quality check
df = wr.athena.read_sql_query(sql=NULL_DQ_CHECK, database="de_proj_database")

# exit if we get a result > 0
# else, the check was successful
if df['myr_col'][0] > 0:
    sys.exit('Results returned. Quality check failed.')
else:
    print('Quality check passed.')

