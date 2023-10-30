import unittest
from awsglue.dynamicframe import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job


class TestGlueJob(unittest.TestCase):

    def setUp(self):
        self.sc = SparkContext()
        self.glueContext = GlueContext(self.sc)
        self.spark = self.glueContext.spark_session
        self.job = Job(self.glueContext)

    def test_datasource0(self):
        datasource0 = self.glueContext.create_dynamic_frame.from_catalog(database="demotesting", table_name="csvdatastorerforse",
                                                            transformation_ctx="datasource0")

        # Assert that the DynamicFrame is not empty
        self.assertGreater(datasource0.count(), 0)

    def test_datasink4(self):
        datasource0 = self.glueContext.create_dynamic_frame.from_catalog(database="demotesting", table_name="csvdatastorerforse",
                                                            transformation_ctx="datasource0")

        datasink4 = self.glueContext.write_dynamic_frame.from_options(frame=datasource0, connection_type="s3",
                                                         connection_options={"path": "s3://serverless/data/"},
                                                         format="parquet",
                                                         transformation_ctx="datasink4")

        # Assert that the data was successfully written to the S3 bucket
        self.assertTrue(self.spark.read.parquet("s3://serverless/data/").count() > 0)


if __name__ == '__main__':
    unittest.main()
