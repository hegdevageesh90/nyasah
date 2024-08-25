import boto3


def create_tenant_table():
    # Initialize DynamoDB client
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',  # Use your DynamoDB endpoint
        aws_access_key_id='local',
        aws_secret_access_key='local',
        region_name='us-west-2'
    )

    # Define table schema
    table = dynamodb.create_table(
        TableName='TenantTable',
        KeySchema=[
            {
                'AttributeName': 'tenant_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'tenant_id',
                'AttributeType': 'S'  # String
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='TenantTable')

    print(f"Table status: {table.table_status}")


if __name__ == "__main__":
    create_tenant_table()
