SELECT
  CAST(day_date AS DATE) AS "date"
  ,myr
FROM free_currency_aud_data_parquet_tbl_prod_2024_09_04_09_31_52_414257 
WHERE $__timeFilter(CAST(day_date AS DATE)) 
ORDER BY 1 
