from fastapi import APIRouter, HTTPException, Depends
from app.models.tenant import Tenant
from app.services.tenant_service import TenantService

router = APIRouter()


def get_tenant_service() -> TenantService:
    return TenantService()


@router.post("/tenants", response_model=dict)
def create_tenant(tenant: Tenant, service: TenantService = Depends(get_tenant_service)):
    try:
        return service.create_tenant(tenant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tenants/{tenant_id}", response_model=dict)
def get_tenant(tenant_id: str, service: TenantService = Depends(get_tenant_service)):
    try:
        return service.get_tenant(tenant_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tenant not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tenants/{tenant_id}", response_model=dict)
def update_tenant(tenant_id: str, updates: dict, service: TenantService = Depends(get_tenant_service)):
    try:
        return service.update_tenant(tenant_id, updates)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tenant not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tenants/{tenant_id}", response_model=dict)
def delete_tenant(tenant_id: str, service: TenantService = Depends(get_tenant_service)):
    try:
        return service.delete_tenant(tenant_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tenant not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tenants", response_model=list)
def list_tenants(service: TenantService = Depends(get_tenant_service)):
    try:
        return service.list_tenants()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
