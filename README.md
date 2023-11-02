## Build Serverless DataLake using AWS Glue, Lambda and Cloudwatch

---

![pipeline](/image/serverless_1.jpg)

### Goals

---

The aim is to create a fully automated data catalogue and ETL pipeline that is explained in detail from scratch.
The data process is very simple: transform raws data into a parquet file


### Tools

---

This ETL architecture uses a serverless approach to extract, transform 
and load data from a CSV file in S3 to a Parquet file in S3. 
The architecture uses the following AWS services:

- **S3** for storing the CSV and Parquet files
- **Glue** for crawling and transforming the data
- **Lambda** for triggering the Glue crawler and job
- **Cloudwatch** for monitoring the Glue crawler and job
- **SNS** for sending notifications

### Architecture Description

---

The ETL process begins when a new CSV file is uploaded to the S3 raw data bucket. A Lambda function is triggered by the S3 event notification. The Lambda function adds the new CSV file to the Glue crawler.

The Glue crawler crawls the S3 raw data bucket periodically and updates the Glue Data Catalog. The Glue Data Catalog provides a metadata layer for the data in S3.

A Cloudwatch rule monitors the status of the Glue crawler. When the Glue crawler finishes crawling the S3 raw data bucket successfully, the Cloudwatch rule triggers a second Lambda function.

The second Lambda function starts the Glue ETL job. The Glue ETL job transforms the CSV data into Parquet format.

The Glue ETL job writes the Parquet data to the S3 processed data bucket. A second Cloudwatch rule monitors the status of the Glue ETL job.

When the Glue ETL job finishes successfully, the Cloudwatch rule sends a notification to an SNS topic. The SNS topic sends an email notification to the user.

### Setup

---

#### 1. S3 Bucket

- Create two buckets:
    - The first for the raw data
    - The second for the processed data

#### 2. Lambda function (trigger the crawler)

**2.1 The code**

[lambda function](crawler%20trigger/crawlertrigger.py)

[test event](crawler%20trigger/testevent.json)

**2.2 triggers**

![crawler](/image/s3_trigger_crawler.png)

**2.3 IAM roles**

- Add to this aws lambda function the ability to access s3 and glue services


![iam](/image/IAM-first.png)


![lambda_iam](/image/lambda-iam.png)

**2.4 General config**

![general](/image/s3-general-config.png)


#### 3. Crawler

**3.1 Create database**

- In glue, go to Data Catalog and create databases (in my case, catalog Database is demotesting)

**3.2 Create Crawler**

- Chose a name for the crawler (in my case, the crawler name is demoserverlesstriggerbasedtechnique)


- Choose data sources

![data_source](/image/data_source.png)

- Configure IAM role

  - Go to IAM, create a new Role and choose **Glue** as **service**

![create_role](/image/IAM-Role-glue.png)

  - Add **S3**, **Glue Service** and **Cloud Watch** to the IAM authorisation

![permission](/image/attached_permission.png)

  - Use this IAM role with the crawler


![IAM_crawler](/image/IAM_crawler.png)

Once the crawler has run, a table will be created with the name of the folder in my S3 basket 
(in my case, the folder in the S3 bucket is csvdatastorerforse)

#### 4. Lambda function (trigger the glue job)

**4.1 The code**

[lambda function](crawler%20trigger/crawlertrigger.py)

**4.2 IAM roles**

- We can use the same IAM role and general configuration as for the previous lambda function

![iam](/image/IAM-first.png)


#### 5. CloudWatch Events


- The purpose of the eventbrigde is to connect two aws services on the basis of a modified event 
(success or failure or simply a change), so that if the state of the Glue crawler becomes a success, 
Cloudwatch will trigger the lambda ETL job


- To create CloudWatch Events, go to CloudWatch then **Rules**


![create_event_crawler](/image/create_event_crawler.png)

- **Crucial**: if we create an event bridge like this, it will trigger the lambda function for each success 
of the glue crawler, and we don't want that,
  we want our crawler, which has the name "demoserverlesstriggerbasedtechnique" to only trigger this event bridge.
To do this, we need to modify the Event pattern by adding the name of the crawler task.


![custom_event_crawler](/image/custom_event_crawler.png)


- select a target witch is the second lambda function 


![target_glue](/image/select_target.png)


The final result will be as follows

![event_glue](/image/event_create.png)


#### 5. Glue job

**5.1 IAM roles**

- First of all, we need to create an IAM role for the glue job and allow it to access glue service, S3 and Cloudwatch

![create_iam_glue](/image/create_iam_glue.png)


![iam-glue](/image/IAM-glue.png)

**5.2 Glue Job**

![glue-job](/image/glue-first.png)

- In the script insert the spark code

[spark code](glue%20job/job.py)

- In the **Job details**, enter the name of the job we are creating on the lambda function, which is "demoserverless"

![glue_job](/image/save_job.png)

