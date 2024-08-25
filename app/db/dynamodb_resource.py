import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class DynamoDBResource:
    def __init__(self, endpoint_url="http://localhost:8000",
                 region_name="us-west-2",
                 access_key_id="local",
                 secret_access_key="local"):
        try:
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=region_name,
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key
            )
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise Exception(f"Error with credentials: {str(e)}")

    def get_table(self, table_name):
        """Returns a DynamoDB table resource."""
        return Table(self.dynamodb.Table(table_name))


class Table:
    def __init__(self, table_resource):
        self.table_resource = table_resource

    def put_item(self, item):
        """Insert or replace an item into the table."""
        return self.table_resource.put_item(Item=item)

    def get_item(self, key):
        """Retrieve an item by key from the table."""
        response = self.table_resource.get_item(Key=key)
        return response.get('Item', None)

    def delete_item(self, key):
        """Delete an item by key from the table."""
        return self.table_resource.delete_item(Key=key)

    def update_item(self, key, update_expression, expression_attribute_values, return_values="UPDATED_NEW"):
        """Update an item in the table."""
        return self.table_resource.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues=return_values
        )

    def query(self, **kwargs):
        """Query the table using various filter criteria."""
        return self.table_resource.query(**kwargs)

    def scan(self, **kwargs):
        """Scan the table."""
        return self.table_resource.scan(**kwargs)
