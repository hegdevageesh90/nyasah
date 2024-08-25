import boto3

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='local',
                          aws_secret_access_key='local',
                          region_name='us-west-2')

# Create the DynamoDB table
table = dynamodb.create_table(
    TableName='Reviews',
    KeySchema=[
        {
            'AttributeName': 'review_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'review_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'product_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'source',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'ProductIndex',
            'KeySchema': [
                {
                    'AttributeName': 'product_id',
                    'KeyType': 'HASH'  # Partition key
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
            'IndexName': 'SourceIndex',
            'KeySchema': [
                {
                    'AttributeName': 'source',
                    'KeyType': 'HASH'  # Partition key
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
    ]
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='Reviews')

print(f"Table {table.table_name} created successfully.")
