import boto3


def create_tenant_table():
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',
        aws_access_key_id='local',
        aws_secret_access_key='local',
        region_name='us-west-2'
    )

    table = dynamodb.create_table(
        TableName='TenantTable',
        KeySchema=[
            {
                'AttributeName': 'tenant_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'tenant_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName='TenantTable')

    print(f"Table status: {table.table_status}")


if __name__ == "__main__":
    create_tenant_table()
