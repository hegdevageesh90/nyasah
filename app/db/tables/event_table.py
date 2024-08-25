import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='local',
                          aws_secret_access_key='local',
                          region_name='us-west-2')


def create_event_table():
    table = dynamodb.create_table(
        TableName='EventTable',
        KeySchema=[
            {
                'AttributeName': 'event_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'event_id',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'tenant_id',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'product_id',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'event_type',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'S'  # String
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'TenantProductIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'tenant_id',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'product_id',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            },
            {
                'IndexName': 'EventTypeTimestampIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'event_type',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='EventTable')

    print(f"Table status: {table.table_status}")


if __name__ == "__main__":
    create_event_table()
