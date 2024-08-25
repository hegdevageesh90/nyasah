import boto3

from app.models.tenant import Tenant


class TenantService:
    def __init__(self):
        self.dynamodb_resource = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8000',
            aws_access_key_id='local',
            aws_secret_access_key='local',
            region_name='us-west-2'
        )
        self.table = self.dynamodb_resource.Table("TenantTable")

    def create_tenant(self, tenant: Tenant) -> dict:
        self.table.put_item(Item=tenant.dict())
        return {"status": "success", "message": "Tenant registered successfully"}

    def get_tenant(self, tenant_id: str) -> dict:
        response = self.table.get_item(Key={'tenant_id': tenant_id})
        item = response.get('Item')
        if not item:
            raise ValueError("Tenant not found")
        return item

    def update_tenant(self, tenant_id: str, updates: dict) -> dict:
        # Update only the provided fields
        update_expression = "set " + ", ".join([f"{k}=:{k}" for k in updates.keys()])
        expression_attribute_values = {f":{k}": v for k, v in updates.items()}

        self.table.update_item(
            Key={'tenant_id': tenant_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {"status": "success", "message": "Tenant updated successfully"}

    def delete_tenant(self, tenant_id: str) -> dict:
        self.table.delete_item(Key={'tenant_id': tenant_id})
        return {"status": "success", "message": "Tenant deleted successfully"}

    def list_tenants(self) -> list:
        response = self.table.scan()
        return response.get('Items', [])
