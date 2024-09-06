SELECT
  CAST(day_date AS DATE) AS "date"
  ,bgn
,brl
,cad
,chf
,cny
,czk
,dkk
,eur
,gbp
,hkd
,hrk
--,huf
--,idr
,ils
,inr
,isk
,jpy
--,krw
,mxn
,myr
,nok
,nzd
,php
,pln
,ron
,rub
,sek
,sgd
,thb
,try
,usd
,zar
FROM free_currency_aud_data_parquet_tbl_prod_2024_09_06_02_39_47_397379 
WHERE $__timeFilter(CAST(day_date AS DATE)) 
ORDER BY 1 
