import boto3

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='local',
                          aws_secret_access_key='local',
                          region_name='us-west-2')

# Create the DynamoDB table
table = dynamodb.create_table(
    TableName='UserGeneratedContent',
    KeySchema=[
        {
            'AttributeName': 'content_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'content_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'content_type',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
    GlobalSecondaryIndexes=[
{
            'IndexName': 'ContentIdIndex',
            'KeySchema': [
                {
                    'AttributeName': 'content_id',
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
            'IndexName': 'UserIdIndex',
            'KeySchema': [
                {
                    'AttributeName': 'user_id',
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
            'IndexName': 'ContentTypeIndex',
            'KeySchema': [
                {
                    'AttributeName': 'content_type',
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
table.meta.client.get_waiter('table_exists').wait(TableName='UserGeneratedContent')

print(f"Table {table.table_name} created successfully.")
