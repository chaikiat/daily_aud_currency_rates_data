# Australian Currency Exchange Rates Data Engineering Pipeline on AWS
This is a data pipeline built in Amazon Web Services (AWS) that fetches the daily Australian currency exchange rates from a currency exchange API, transforms the data into a format that is finally visualized onto a Grafana dashboard. 

## Content
[1) Objective](#1-objective)
<br>[2) Technology used](#2-technology-used)
<br>[3) Architectural diagram of pipeline](#3-architectural-diagram-of-pipeline)
<br>[4) Data source](#4-data-source)
<br>[5) Implementation steps](#5-implementation-steps)
<br>[6) Grafana dashboard](#6-grafana-dashboard)
<br>[7) Grafana dashboard snapshots](#7-grafana-dashboard-snapshots)
<br>[8) Additional opportunities](#8-additional-opportunities)
<br>[9) Documentation](#9-documentation)

## [1) Objective](#1-objective)
Instead of checking exchange rates online, this pipeline enables the fully automated flow of Australian currency exchange data into a dashboard that enables easier monitoring, alerting of currency fluctuations to better inform decisions over when to execute foreign exchange transactions. 

## [2) Technology Used](#2-technology-used)
      a. For scripting: Python and SQL
      b. For data ingestion: AWS Lambda, Amazon Data Firehose
      c. For orchestration, data transformation: AWS Glue
      d. For storage: AWS S3
      e. For data queries: Amazon Athena
      f. For data visualisation: Grafana

## [3) Architectural Diagram of Pipeline](#3-architectural-diagram-of-pipeline)
![de_project_currency_ck drawio](https://github.com/user-attachments/assets/57dc3050-4dba-4602-8257-4bd356cf68f4)

## [4) Data Source](#4-data-source)
   a. Data provider: [Free Currency API](https://freecurrencyapi.com)
   b. Authentication to the API is via an API key, which can be generated when you sign up for free 

## [5) Implementation Steps](#5-implementation-steps)
      1. In AWS, go to Lambda and create a Python function - Python runtime, x86_64 architecture
      2. In the Lambda code source, use this file in the repository as the source code - [src/lambda/free_currency_api_extract_latest.py]
      3. Create a free account on https://freecurrencyapi.com, and generate an API key
      4. In the Lambda Python code, add the API key into the `apikey` query parameter in the URL under the variable r
      5. The `base_currency` query parameter I used is AUD, you can change it to any other base currency
      6. In AWS S3, create a new bucket for your API data to be stored in
      7. In Amazon Data Firehose, create a Firehose stream - source = Direct PUT, destination = Amazon S3, S3 bucket = the bucket created in #6           above
      8. Go back to the Lambda function, save your Python script and Deploy. 
      9. Test to invoke the Lambda function, a status = 200 response indicates a working Python script making the request. 
      10. Add a trigger for the function for daily automated invocation of the function, by using EventBridge (CloudWatch Events) trigger type -           schedule expression: rate(1 day)
      11. In AWS Glue, create a Crawler to crawl your files in the S3 bucket and create partitioned tables in Amazon Athena - data source = your           S3 bucket (#6 above)
      12. In AWS Glue, go to ETL jobs and create a job using Script editor
      13. Create a job each for the glue job files in the repository - [src/glue_jobs]
          a. `delete_parquet_currency_table_s3_athena.py`: drops the table in S3, in order to create a new table with every run of the ETL job
          b. `create_parquet_currency_table_glue_job.py`: references the raw API data table (#6 above) and creates a new partitioned table
          c. `dq_checks_parquet_currency_table.py`: Runs a series of data quality checks on the new table, to validate for any unintended data                in the table
          d. `publish_prod_parquet_currency_table.py`: Publishes the final table in a production database in Amazon Athena, where downstream applications like Grafana can access
      14. In AWS Glue, create a workflow to orchestrate this data pipeline:
          a. Start the pipeline every day or on-demand (to trigger the pipeline manually)
          b. Next, run the crawler (#11 above)
          c. Next, trigger the delete table job to be started by after the previous watched event
          d. Next, run the delete table job (#13a above)
          e. Next, trigger to run the create table job (#13b above) to be started after the previous watched event (#14d above)
          f. Next, trigger to run the data quality checks job (#13c above) to be started after the previous watched event (#14e above)
          g. Next, trigger to publish to production Athena database (#13d above) to be started after the previous watched event (#14f above)
      15. Run the AWS glue workflow
      16. In Amazon Athena, there will be a newly created Parquet table which can be used for any downstream applications (eg. Grafana to build a dashboard)
      17. Create a free account in Grafana, and log in
      18. Add a new connection in Grafana - data source - Amazon Athena
      19. Install the Amazon Athena connector, and the add a new datasource
      20. In AWS IAM, create a new user and attach the policies `AmazonAthenaFullAccess` and `AmazonS3FullAccess`. And create access key.
      21. In Grafana and under Connection Details, you will need to add the Access Key ID and Secret Access Key that you created from #20 above. 
      22. In Grafana , write a SQL query or use the SQL file in the repository query data from Athena in a way that Grafana can visualize on a dashboard - [src/sql/grafana_currency_query]
      23. Create your customised visualisations to build your dashboard

## [6) Grafana dashboard](#6-grafana-dashboard)
<img width="1464" alt="grafana_dashboard_aud_daily_conversion" src="https://github.com/user-attachments/assets/7481f06b-8538-46fd-a5a1-2617e32a55d6">

## [7) Grafana dashboard snapshots](#7-grafana-dashboard-snapshots)
a. [Snapshot 1: Scorecards - Australian Currency - Daily Exchange Rates - Grafana - Dashboards](https://ckkho.grafana.net/dashboard/snapshot/oPy2IbVXeI96t4ad84TgcplsXY1rr8sV)<br>
b. [Snapshot 2: Daily trend - AUD to MYR Currency - Daily Exchange Rates - Grafana - Dashboards](https://ckkho.grafana.net/dashboard/snapshot/2wmMEzp9kepDx8eFA9fYtXlAcEFX8Web)<br>
c. [Snapshot 3: Daily trend - AUD to USD Currency - Daily Exchange Rates - Grafana - Dashboards
](https://ckkho.grafana.net/dashboard/snapshot/EQo5RRdH28v6cEAx1rKT6ZTf10mA2EjA)<br>
d. [Snapshot 4: Daily trend - AUD to SGD Currency - Daily Exchange Rates - Grafana - Dashboards
](https://ckkho.grafana.net/dashboard/snapshot/xtGmRt7pXwiBNgkFVoFQPE3265MTxKCP)<br>
e. [Snapshot 5: Daily trend - AUD to all currencies - Daily Exchange Rates - Grafana - Dashboards
](https://ckkho.grafana.net/dashboard/snapshot/8EYJyjoH4rM8yonEHgECpAywlNmedv2L)<br>

## [8) Additional opportunities](#8-additional-opportunities)
This pipeline can be extended to more base currencies and longer lookback in historical data, in order to report on more trends around more currencies. Advanced analytics opportunities include training the production dataset on linear regression to build a predictive model on currency fluctuations, or even feeding into large language models (LLMs) to relate the data to world events for more context over the fluctuations.

## [9) Documentation](#9-documentation)
a. [Free currency api](https://freecurrencyapi.com/docs)<br>
b. [AWS Glue workflows](https://docs.aws.amazon.com/glue/latest/dg/workflows_overview.html)<br>
c. [Grafana dashboard](https://grafana.com/docs/grafana/latest/dashboards/)
***
